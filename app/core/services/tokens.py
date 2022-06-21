from typing import List
from fastapi import Request
from app.core.config import config
from app.core.constants import BEARER
from app.core.services.users import get_user
from app.core.security import verify_password, CredentialException, createJWT
from app.core.schemas.users import User
from app.core.schemas.tokens import Token, TokenData, TokenUser
from app.utils.localization import _
from app.core.database import connection


async def authenticate_user(username: str, password: str) -> User:
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def createToken(req: Request, user: User, scopes: List = []) -> Token:
    if not user:
        raise CredentialException(_(req, 'errors.auth.invalid_credentials'), authenticate_value=BEARER)
    req.state.user = user
    access_token = createJWT(TokenData(user=TokenUser(id=user.id, username=user.username, description=user.description), scopes=scopes))
    refresh_token = createJWT(TokenData(user=TokenUser(id=user.id, username=user.username, description=user.description), scopes=scopes), ttl=config.security.REFRESH_TOKEN_TTL)
    await connection.execute(
        query='insert into acl_token(role_id, access_token, refresh_token) values (:role_id, :access_token, :refresh_token) on conflict(role_id) do update set access_token = :access_token, refresh_token = :refresh_token',
        values={'role_id': req.state.user.id, 'access_token': access_token, 'refresh_token': refresh_token}
        )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type=BEARER)


async def isNotActiveToken(token:str, is_refresh: bool = False):
    query = f'select count(0) > 0 as result from acl_token where {"refresh" if is_refresh else "access"}_token = :token'
    data = await connection.fetch_one(query=query, values={'token': token})
    if data.result:
        return False
    return True