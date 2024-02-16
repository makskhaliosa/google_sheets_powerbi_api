import logging
from typing import Dict, List

from pbipy.datasets import Dataset
from pbipy.reports import Report

from extended_pbipy.entities import DatasetCreate, Table
from extended_pbipy.enums import ColumnDataTypes
from extended_pbipy.table_items import Column
from src.core.config import settings
from .google_api import get_values, get_file, get_sheet_titles
from .pbi_api import pbi


logger = logging.getLogger(__name__)


class ApiExchangeFlowAllMarket:
    '''Класс для создания датасета по листу Весь рынок.'''

    def __init__(
            self,
            sheet_id: str,
            pbi_report_id: str
    ):
        self.sheet_id = sheet_id
        self.table_file = self._get_file_name(self.sheet_id)
        self.report_id = pbi_report_id
        self._table_rows = {}

    def _get_table_values(self, sheet_id: str, cell_range: str) -> List[List]:
        '''Запрашивает данные из гугл таблицы по ее id.'''
        sheet_data = get_values(sheet_id, cell_range)
        logger.info(f'Received data from {cell_range}')
        return sheet_data.get('values')

    def _get_file_name(self, sheet_id: str) -> str:
        '''
        Запрашивает данные о файле гугл таблицы.

        Возвразает имя файла.
        '''
        file = get_file(sheet_id)
        return file.get('name')

    def _get_titles(self, sheet_id: str) -> Dict:
        '''Вернуть все названия листов файла.'''
        return get_sheet_titles(sheet_id)

    def _get_columns(self, values: List[List]):
        '''Извлекает заголовки столбцов.'''
        columns = values[1]
        columns[0] = '№'
        first_part = columns[:31]
        second_part = columns[31:]
        new_part = [
            'Категория.1', 'Категория.2', 'Категория.3',
            'Категория.4', 'Категория.5'
        ]
        columns = first_part + new_part + second_part
        return columns

    def _create_pbi_table(
            self,
            column_headers: List,
            table_name: str
    ) -> Table:
        '''
        Создает объект таблицы со столбцами, как первая строка в таблице гугл.
        '''
        new_table = Table(name=table_name)

        data_types = {
            ColumnDataTypes.Int64: [
                7, 12, 15, 16, 17, 18, 19, 20, 21, 28, 29, 36, 37, 38
            ],
            ColumnDataTypes.Currency: [8, 10, 11],
            ColumnDataTypes.Datetime: [13],
            ColumnDataTypes.Double: [9, 10, 11, 14],
            ColumnDataTypes.Boolean: [22]
            # строковые значения [1, 2, 3, 4, 5, 6, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 39, 40, 41, 42]
        }

        if column_headers:
            for header_idx in range(len(column_headers)):
                format_string = ''

                try:
                    data_type = ColumnDataTypes.String
                    for k, v in data_types.items():
                        if header_idx in v:

                            if k == ColumnDataTypes.Currency:
                                data_type = ColumnDataTypes.Double
                                format_string = 'Currency'
                            else:
                                data_type = k
                            break
                except IndexError:
                    logger.error('Index error in create pbi table.')
                    data_type = 'String'

                column_name = column_headers[header_idx]

                column = Column(
                    name=column_name,
                    data_type=data_type,
                    format_string=format_string
                )
                new_table.add_column(column)

        return new_table

    def _add_rows(self, table: Table, table_rows: List) -> Table:
        '''Добавляет строки в таблицу PowerBI.'''
        self._table_rows[table.name] = []
        table_columns = table.columns
        int_values = [7, 8, 10, 11, 12, 29, 31, 32, 33]
        double_values = [14]
        bool_values = [22]
        cities = [
            'Москва', 'Санкт-Петербург', 'Казань', 'Краснодар',
            'Екатеринбург', 'Новосибирск', 'Хабаровск'
        ]

        # Добавляются столбцы с подкатегориями
        categories = {
            'Категория.1': '',
            'Категория.2': '',
            'Категория.3': '',
            'Категория.4': '',
            'Категория.5': '',
        }
        shifted = False

        for row in table_rows:
            row_data = {}
            for value_num in range(len(row)):

                try:
                    # Учитываем смещение индекса после разделения на подкатегории
                    column_idx = value_num + 5 if shifted else value_num
                    column_name = table_columns[column_idx].name
                    row_value = (
                        row[value_num] if row[value_num] else ''
                    )
                    if '₽' in row_value:
                        row_value = row_value.replace('₽', '')
                    if value_num in int_values:
                        if not row_value:
                            row_value = 0
                        else:
                            row_value = ''.join(row_value.split())
                    elif column_name in cities:
                        if not row_value:
                            row_value = 0
                    elif value_num in double_values and not row_value:
                        row_value = 0.0
                    elif value_num in bool_values and not row_value:
                        row_value = False

                    row_data[column_name] = row_value

                    if column_name == 'Категория':
                        shifted = True
                        # Делим на подкатегории
                        keys = list(categories.keys())
                        sub_categories = row_value.split('/')
                        last_idx = len(sub_categories) - 1
                        for k_idx in range(len(keys)):
                            if last_idx >= 0:
                                last_idx -= 1
                                categories[keys[k_idx]] = sub_categories[k_idx]
                            else:
                                break
                        for k, v in categories.items():
                            row_data[k] = v

                    if value_num == len(row) - 1:
                        shifted = False

                except IndexError:
                    logger.error('Index error in add rows', exc_info=True)
                    column_name = 'Undefined'
                    row_data[column_name] = row_value

                except Exception as err:
                    logger.error(f'Error in add rows {err}', exc_info=True)
                    column_name = 'Undefined'
                    row_data[column_name] = row_value

            self._table_rows[table.name].append(row_data)

    def _create_dataset(self) -> DatasetCreate:
        '''
        Создает объект DatasetCreate с таблицей данных.

        Создает словарь с названием таблицы и ее строками.
        '''
        new_dataset = DatasetCreate(name=self.table_file)
        for range_title in get_sheet_titles(self.sheet_id):
            try:
                values = self._get_table_values(self.sheet_id, range_title)

                columns = self._get_columns(values)

                # Создать таблицу со столбцами и типами данных
                pbi_table = self._create_pbi_table(
                    columns,
                    range_title
                )

                # Создаем словарь с соответствием столбца и строк
                if len(values) > 2:
                    self._add_rows(pbi_table, values[3:])

                new_dataset.add_table(pbi_table)
            except Exception as err:
                logger.error(f'Error create dataset {err}', exc_info=True)

        new_dataset.clear_empty_data()

        return new_dataset

    def _push_dataset(self) -> Dataset:
        '''
        Отправляет данные в PowerBI.

        Возвращает созданный Dataset и список созданных таблиц.
        '''
        new_dataset = self._create_dataset()
        dataset_created = pbi.post_group_dataset(
            group=settings.PBI_GROUP,
            dataset=new_dataset,
            default_retention_policy=None
        )
        return dataset_created

    def _post_dataset_rows(
            self,
            dataset: Dataset,
            table_name: str,
            table_rows: List
    ) -> None:
        '''Отправляет запрос на добавление строки в таблицу.'''
        logger.info(f'Adding rows to table {table_name}')

        pbi.post_group_dataset_rows(
            group_id=dataset.group_id,
            dataset_id=dataset.id,
            table_name=table_name,
            rows=table_rows
        )
        logger.info('Added rows to table.')

    def run(self) -> Report:
        '''
        Запускает процесс переноса данных из гугл таблицы.

        Создается таблица с данными в PowerBI и
        подключается к клонированному отчету.
        '''
        try:
            logger.info('Starting data transfer.')
            dataset = self._push_dataset()
            for table, rows in self._table_rows.items():
                self._post_dataset_rows(dataset, table, rows)
            logger.info('Data transfer finished.')

            logger.info(f'Cloning report {self.report_id}')

            cloned_report = pbi.report(
                report=self.report_id, group=settings.PBI_GROUP
            ).clone(name=self.table_file, target_dataset=dataset.id)

            logger.info(f'Report {self.report_id} cloned.')

            return cloned_report

        except Exception as err:
            logger.error(f'Error in data transfer {err}.', exc_info=True)
