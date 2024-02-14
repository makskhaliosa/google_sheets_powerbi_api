import logging
from typing import Dict, List, Tuple

from pbipy.datasets import Dataset
from pbipy.reports import Report

from extended_pbipy.entities import DatasetCreate, DataSource, Table
from extended_pbipy.enums import ColumnDataTypes, DataSourceType
from extended_pbipy.table_items import Column
from src.core.config import settings
from .google_api import get_values, get_file, get_sheet_titles
from .pbi_api import pbi


logger = logging.getLogger(__name__)


class ApiExchangeFlow:
    '''Класс для управления создания нового объекта DatasetCreate.'''

    def __init__(
            self,
            sheet_id: str,
            pbi_report_id: str
    ):
        self.sheet_id = sheet_id
        self.table_file = self._get_file_name(self.sheet_id)
        self.report_id = pbi_report_id
        self._table_rows = {}
        # self.cell_values = self._get_table_values(self.sheet_id)

        # self.column_headers = None
        # if self.cell_values:
        #     self.column_headers = self._get_column_headers(self.cell_values)
        #     self.cell_values.remove(self.column_headers)

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

    def _get_longest_row(self, values: List[List]):
        '''Извлекает заголовки столбцов.'''
        longest = 0
        for row_num in range(len(values[1:10])):
            if len(values[longest]) < len(values[row_num]):
                empty_value = False
                for item in values[row_num]:
                    if not item:
                        empty_value = True
                        break
                if not empty_value:
                    longest = row_num
        return longest

    def _create_pbi_table(
            self,
            column_headers: List,
            row_values: List,
            table_name: str
    ) -> Table:
        '''
        Создает объект таблицы со столбцами, как первая строка в таблице гугл.
        '''
        new_table = Table(name=table_name)
        empty_name_counter = 0

        if column_headers:
            for header_idx in range(len(column_headers)):

                try:
                    data_type = ColumnDataTypes.convert_from_python(
                        row_values[header_idx]
                    )
                except IndexError:
                    logger.error('Index error in create pbi table.')
                    data_type = 'String'

                column_name = column_headers[header_idx]
                if not column_headers[header_idx]:
                    empty_name_counter += 1
                    column_name = f'Undefined {empty_name_counter}'
                column = Column(
                    name=column_name,
                    data_type=data_type
                )
                new_table.add_column(column)

        return new_table

    def _add_rows(self, table: Table, table_rows: List) -> Table:
        '''Добавляет строки в таблицу PowerBI.'''
        self._table_rows[table.name] = []
        table_columns = table.columns

        for row in table_rows:
            row_data = {}
            for value_num in range(len(row)):

                try:
                    column_name = table_columns[value_num].name
                    row_value = (
                        row[value_num] if row[value_num] else '--Empty--'
                    )
                    row_data[column_name] = row_value

                except IndexError:
                    logger.error('Index error in add rows')
                    column_name = 'Undefined'
                    row_data[column_name] = row_value

                except Exception as err:
                    logger.error(f'Error in add rows {err}', exc_info=True)
                    column_name = 'Undefined'
                    row_data[column_name] = row_value

            self._table_rows[table.name].append(row_data)

        # return table

    def _create_dataset(self) -> DatasetCreate:
        '''
        Создает объект DatasetCreate с таблицей данных.

        Подключает DataSource к таблице гугл по url.
        '''
        new_dataset = DatasetCreate(name=self.table_file)
        for range_title in get_sheet_titles(self.sheet_id):
            try:
                values = self._get_table_values(self.sheet_id, range_title)
                # Найти самую длинную строку (предполагаемо заголовок)
                longest = self._get_longest_row(values)
                # Создать таблицу со столбцами и типами данных, как в строках ниже
                row_with_data = (
                    longest + 2
                    if len(values) - 2 > longest
                    else longest
                )

                pbi_table = self._create_pbi_table(
                    values[longest],
                    values[row_with_data],
                    range_title
                )
                # Берем строки ниже предполагаемого заголовка
                self._add_rows(pbi_table, values[longest:])
                new_dataset.add_table(pbi_table)
            except Exception as err:
                logger.error(f'Error create dataset {err}', exc_info=True)

        connection_details = {
            'path': f'{settings.SHEETS_URL}/{self.sheet_id}',
            'kind': 'GoogleSheets'
        }
        datasource = DataSource(
            data_source_type='Web',
            connection_details=connection_details
        )
        # new_dataset.add_data_source(datasource)

        new_dataset.clear_empty_data()
        print(new_dataset)

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

    def _post_dataset_rows(self, dataset: Dataset, table_name: str, table_rows: List) -> None:
        '''Отправляет запрос на добавление строки в таблицу.'''
        logger.info(f'Adding rows to table {table_name}')

        # table = self._add_rows(table)
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
            # return dataset

        except Exception as err:
            logger.error(f'Error in data transfer {err}.', exc_info=True)
