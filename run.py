import uvicorn

from src.api.handlers import pbi_router
from src.core.config import app, LOGGING_CONFIG, settings

app.include_router(pbi_router)


if __name__ == '__main__':
    uvicorn.run(
        app='run:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_config=LOGGING_CONFIG
    )
