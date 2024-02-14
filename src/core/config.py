from logging import config

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True
    )

    TITLE: str = 'PBI_API'
    HOST: str
    PORT: int
    ALLOWED_ORIGINS: str
    GAPI_CREDS: str
    GAPI_SCOPES: str
    GAPI_URL: str
    PBI_AUTH_URL: str
    PBI_CLIENT_ID: str
    PBI_CLIENT_SECRET: str
    PBI_SCOPES: str
    PBI_GROUP: str
    SHEETS_URL: str


settings = Settings()

# Конфиг логера
config.dictConfig(LOGGING_CONFIG)

# Конфиг fastapi
app = FastAPI(
    title=settings.TITLE,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)
