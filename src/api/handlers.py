import logging

from fastapi import APIRouter

from src.schemas.entities import ReportData, ReportRequestData, SheetReportID
from src.services.api_exchange_v2 import ApiExchangeFlowAllMarket

logger = logging.getLogger(__name__)

pbi_router = APIRouter()


@pbi_router.post(path='/run_app', response_model=ReportData)
async def run_app(data: SheetReportID) -> ReportData:
    '''URL для запуска процесса переноса данных в отчет PBI.'''
    sheet_id = data.google_sheet_id
    report_id = data.pbi_report_id

    exchange = ApiExchangeFlowAllMarket(
        sheet_id=sheet_id,
        pbi_report_id=report_id
    )
    new_report = exchange.run()
    # print(new_report)
    report_data = ReportData(report_id=new_report.id, embed_url='url')

    return report_data


@pbi_router.get(path='/get_report', response_model=ReportData)
async def get_report(report_data: ReportRequestData) -> ReportData:
    '''URL для запроса данных отчета.'''
    return ReportData
