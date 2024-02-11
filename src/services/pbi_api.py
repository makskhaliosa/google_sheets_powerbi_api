from typing import Any, Dict, List

from msal import ConfidentialClientApplication

from extended_pbipy.pbi_client import ExtendedPowerBI
from src.core.config import settings


def get_token(
        scope: List[str],
        auth_url: str,
        client_id: str,
        client_secret: str
) -> Dict[str, Any]:
    '''Возвращает токен для работы с API PowerBI.'''

    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=auth_url
    )
    result = app.acquire_token_for_client(scopes=scope)
    return result.get('access_token')


pbi_token = get_token(
    scope=settings.PBI_SCOPES,
    auth_url=settings.PBI_AUTH_URL,
    client_id=settings.PBI_CLIENT_ID,
    client_secret=settings.PBI_CLIENT_SECRET
)

pbi = ExtendedPowerBI(bearer_token=pbi_token)
