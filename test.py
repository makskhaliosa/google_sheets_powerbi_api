from pprint import pprint
from extended_pbipy.entities import DatasetCreate, Table, DataSource
from extended_pbipy.table_items import Column
from src.services.google_api import get_values, get_file, get_sheet_titles
from src.services.pbi_api import pbi
from src.services.api_exchange import ApiExchangeFlow
from src.services.api_exchange_v2 import ApiExchangeFlowAllMarket
# pprint(get_values(sheet_id='1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY', cell_range='A:Z'))
# pprint(get_file(file_id='1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY'))


# reports = pbi.reports(group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b')
# print(reports)

# flow = ApiExchangeFlow(sheet_id='1wRE_vvSbE2V3tDhMbzTOVcSbn-A738WUdZ6dPlZAOc0', pbi_report_id='26424232-dbfb-4855-b7b5-a87d147a3195')
# data = flow.run()

flow = ApiExchangeFlowAllMarket(sheet_id='1ZIP5Zca0xur_o3sxDuE_LPBCaDeuz2xePQCcnq9GZuI', pbi_report_id='26424232-dbfb-4855-b7b5-a87d147a3195')
data = flow.run()

# print(data)

#take = pbi.dataset(group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b', dataset='c858bff2-c493-44dc-a8d2-316e580de5fa').take_over()
#print(take)

# boards = pbi.dashboards_in_group(group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b')
# print(boards)

# for title in get_sheet_titles('1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY'):
#     print(title)
#     value = get_values('1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY', title)
#     print(value)

# report = pbi.report(report='26424232-dbfb-4855-b7b5-a87d147a3195', group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b')
# dataset = pbi.dataset(dataset=report.dataset_id, group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b')
# # print(report)
# # print(report.datasources())
# # print(dataset.parameters())
# tables = pbi.get_group_tables(group_id=dataset.group_id, dataset_id=dataset.id)
# print(tables)

# print(dataset.update_parameters(
#     update_details={
#         "name": "datasourceSelector",
#         "newValue": "Web"
#         "connectionDetails": {
#             "path": "https://docs.google.com/spreadsheets/d/1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY/edit#gid=750438175",
#             "kind": "GoogleSheets"
#         },
#         "datasourceId": "cc1e95c1-ff55-46ab-bc3f-34a2ea07687e",
#         "gatewayId": "f099cce0-680d-4532-8070-bc31d8290d71"
#     }
# )
# )

# new_report = pbi.report(
#     report='cb2318aa-ac74-4ab8-b0af-3943604a5d98', group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b'
# ).clone(name='new_test', target_group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b', target_dataset='56b96d8c-f37e-42cc-91d8-56a0c5c026bf')

# data = DatasetCreate(name='trial2')
# table = Table(name='Table')
# column = Column(name='Col', data_type='String')
# datasource = DataSource(data_source_type='Web', connection_details={"path": "https://docs.google.com/spreadsheets/d/1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY/edit#gid=750438175", "kind": "GoogleSheets"})
# table.add_column(column)
# data.add_table(table)
# data.add_data_source(datasource)

# print(data.data_sources)


# new_dataset = pbi.post_group_dataset(group='d61bf643-1710-4bfd-bf79-5d53fdc89e9b', dataset=data)

# print(new_dataset)
# print(new_dataset.datasources())


# sheets = get_sheets('1lJ_wQ_4xPVn1bA-SbGmRgfkIUMxBe56Q1qk6DGVEsQY')
# print(sheets)
