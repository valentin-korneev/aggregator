from datetime import datetime
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from time import time, mktime
from core.config import config
from fastapi.security.utils import get_authorization_scheme_param
from core.constants import BEARER
from core.services.users import get_user_from_token, log_request
from utils.localization import _


async def setRequestTimeMiddleware(req: Request, call_next) -> Response:
    req.state.request_time = datetime.now()
    resp = await call_next(req)
    return resp


async def processTimeHeaderMiddleware(req: Request, call_next) -> Response:
    resp = await call_next(req)
    resp.headers['X-Process-Time'] = str(time() - (mktime(req.state.request_time.timetuple()) + req.state.request_time.microsecond / 1E6))
    return resp


async def languageHeaderMiddleware(req: Request, call_next) -> Response:
    req.state.language = req.headers.get('X-Language', config.language.DEFAULT)
    resp = await call_next(req)
    resp.headers['X-Language'] = req.state.language
    return resp


async def setUserMiddleware(req: Request, call_next) -> Response:
    authorization: str = req.headers.get('Authorization')
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != BEARER.lower() or req.scope['path'].split('/')[-2:] == ['token', 'refresh']:
        req.state.user = None
    else:
        req.state.user = await get_user_from_token(req, param)
        if req.state.user is None:
            return JSONResponse(content={'detail': _(req, 'errors.auth.compromised_credential')}, status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': BEARER})
            
    resp = await call_next(req)
    if req.state.user is not None:
        await log_request(req, resp)
    return resp