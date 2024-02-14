import logging
from typing import Any, Dict, List

from msal import ConfidentialClientApplication

from extended_pbipy.pbi_client import ExtendedPowerBI
from src.core.config import settings

logger = logging.getLogger(__name__)


def get_token(
        scope: List[str],
        auth_url: str,
        client_id: str,
        client_secret: str
) -> Dict[str, Any]:
    '''Возвращает токен для работы с API PowerBI.'''

    try:
        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=auth_url
        )
        result = app.acquire_token_silent(scopes=scope, account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=scope)
        return result.get('access_token')
    except Exception as err:
        logger.error(f'Error get token {err}', exc_info=True)


pbi_token = get_token(
    scope=settings.PBI_SCOPES.split(),
    auth_url=settings.PBI_AUTH_URL,
    client_id=settings.PBI_CLIENT_ID,
    client_secret=settings.PBI_CLIENT_SECRET
)

pbi = ExtendedPowerBI(bearer_token=pbi_token)
