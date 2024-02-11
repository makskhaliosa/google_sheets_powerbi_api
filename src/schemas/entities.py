from pydantic import BaseModel


class SheetReportID(BaseModel):
    '''Схема данных для запуска процесса переноса данных.'''
    google_sheet_id: str
    pbi_report_id: str


class ReportData(BaseModel):
    '''Схема данных отчета для фронтенда.'''
    report_id: str
    embed_url: str


class ReportRequestData(BaseModel):
    '''Схема данных для запроса данных отчета.'''
    pbi_report_id: str
