from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from core.database import shutdown, startup
from core.enums.environment import EnvironmentState
from core.middleware import languageHeaderMiddleware, processTimeHeaderMiddleware, setRequestTimeMiddleware, setUserMiddleware
from api import tokens, users
from core.config import config, logger


app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=setUserMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=languageHeaderMiddleware)
if config.environment.STATE == EnvironmentState.DEVELOPMENT:
    app.add_middleware(BaseHTTPMiddleware, dispatch=processTimeHeaderMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=setRequestTimeMiddleware)

app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)

app.include_router(tokens.router, tags=['tokens'])
app.include_router(users.router, tags=['users'])

config.logging.init()
logger.info('Логирование успешно настроено')
