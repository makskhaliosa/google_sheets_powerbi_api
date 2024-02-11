import logging
from typing import Any, Dict

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
# from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

from src.core.config import settings

logger = logging.getLogger(__name__)


def get_credentials() -> Credentials:
    '''Возвращает объект с данными для авторизации через сервисный аккаунт.'''
    creds = Credentials.from_service_account_file(
      filename=settings.GAPI_CREDS,
      scopes=settings.GAPI_SCOPES.split()
    )
    return creds


def get_tables_service() -> Resource:
    '''Возврщает объект для взаимодействия Google API.'''
    creds = get_credentials()
    return build('sheets', 'v4', credentials=creds)


def get_drive_service() -> Resource:
    '''Возврщает объект для взаимодействия Google API.'''
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)


def get_file(file_id: str) -> Dict[str, Any]:
    '''Возвращает инфо о файле с гугл диска по id файла.'''
    client = get_drive_service()
    file = client.files().get(fileId=file_id).execute()
    return file


def get_values(sheet_id: str, cell_range: str = None) -> Dict[str, Any]:
    '''
    Возвращает список со значениями заданных ячеек из заданной таблицы.

    По умолчанию cell_range охватывает все стобцы и строки от A до Z.'''
    try:
        if cell_range is None:
            cell_range = 'A:Z'
        client = get_tables_service()
        sheet = client.spreadsheets()
        values = sheet.values().get(
            spreadsheetId=sheet_id, range=cell_range
        ).execute()
        return values
    except Exception as err:
        logger.error(f'Error getting values {err}', exc_info=True)
