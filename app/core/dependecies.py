
from fastapi import Request, Depends
from fastapi.security import SecurityScopes
from app.core.constants import BEARER
from app.core.security import ForbiddenException, OAuth2PasswordBearer
from app.core.schemas.users import User
from app.core.services.users import check_assignment
from app.utils.localization import _


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token', refreshUrl='/token/refresh', scopes={'scope': 'description'})


async def get_current_user(req: Request, security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> User: # oauth2_scheme - TO_DO: remove (need for security key in Swagger)
    user = req.state.user
    if security_scopes.scopes:
        if not await check_assignment(user.id, security_scopes.scopes):
            raise ForbiddenException(
                _(req, 'errors.auth.forbidden'),
                authenticate_value=BEARER
            )
    return user


async def get_current_active_user(req: Request, current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise ForbiddenException(_(req, 'errors.auth.inactive'))
    return current_user