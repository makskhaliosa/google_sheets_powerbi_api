import logging
from typing import List

from pbipy.reports import Report

from extended_pbipy.entities import DatasetCreate, DataSource, Table
from extended_pbipy.enums import ColumnDataTypes, DataSourceType
from extended_pbipy.table_items import Column
from src.core.config import settings
from .google_api import get_values, get_file
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
        self.table_file = self._get_table_file_name(self.sheet_id)
        self.report_id = pbi_report_id
        self.cell_values = self._get_table_values(self.sheet_id)

        self.column_headers = None
        if self.cell_values:
            self.column_headers = self.cell_values[0]

    def _get_table_values(self, sheet_id: str) -> List[List]:
        '''Запрашивает данные из гугл таблицы по ее id.'''
        sheet_data = get_values(sheet_id)
        logger.info(f'Received data from {self.sheet_id}')
        return sheet_data.get('values')

    def _get_table_file_name(self, sheet_id: str) -> str:
        '''
        Запрашивает данные о файле гугл таблицы.

        Возвразает имя файла.
        '''
        file = get_file(sheet_id)
        return file.get('name')

    def _create_pbi_table(self) -> Table:
        '''
        Создает объект таблицы со столбцами, как первая строка в таблице гугл.
        '''
        new_table = Table(name=self.table_file)

        if self.column_headers:
            for header in self.column_headers:
                data_type = ColumnDataTypes.convert_from_python('uncertain')
                column = Column(name=header, data_type=data_type)
                new_table.add_column(column)
                new_table.add_measure = data_type

        return new_table

    def _add_rows(self) -> Table:
        '''Добавляет строки в таблицу PowerBI.'''
        pbi_table = self._create_pbi_table()
        table_columns = pbi_table.columns
        google_table_rows = self.cell_values[1:]

        for row in google_table_rows:
            row_data = {}
            for value_num in range(len(row)):

                try:
                    column_name = table_columns[value_num].name
                    row_data[column_name] = row[value_num]

                except IndexError as err:
                    logger.error(
                        f'Index error in add rows {err}', exc_info=True
                    )
                    column_name = 'Undefined'
                    row_data[column_name] = row[value_num]

                except Exception as err:
                    logger.error(f'Error in add rows {err}', exc_info=True)
                    column_name = 'Undefined'
                    row_data[column_name] = row[value_num]

            pbi_table.add_row(row_data)

        return pbi_table

    def _create_dataset(self) -> DatasetCreate:
        '''
        Создает объект DatasetCreate с таблицей данных.

        Подключает DataSource к таблице гугл по url.
        '''
        pbi_table = self._add_rows()
        new_dataset = DatasetCreate(name=self.table_file.get('name'))
        new_dataset.add_table(pbi_table)

        connection_details = {'url': f'{settings.GAPI_URL}/{self.sheet_id}'}
        datasource = DataSource(
            DataSourceType.GoogleSheets,
            connection_details
        )
        new_dataset.add_data_source(datasource)

        return new_dataset

    def _push_dataset(self):
        '''Отправляет данные в PowerBI.'''
        new_dataset = self._create_dataset()
        dataset_created = pbi.post_dataset(new_dataset)
        return dataset_created

    def run(self) -> Report:
        '''
        Запускает процесс переноса данных из гугл таблицы.

        Создается таблица с данными в PowerBI и
        подключается к клонированному отчету.
        '''
        try:
            logger.info('Starting data transfer.')
            dataset = self._push_dataset()
            logger.info('Data transfer finished.')

            logger.info(f'Cloning report {self.report_id}')

            cloned_report = pbi.report(
                report=self.report_id
            ).clone(name='New Report', target_dataset=dataset)

            logger.info(f'Report {self.report_id} cloned.')

            return cloned_report

        except Exception as err:
            logger.error(f'Error in data transfer {err}.', exc_info=True)
