
from typing import List
from fastapi import Request
from core.config import config
from core.constants import BEARER
from core.services.users import get_user, log_request
from core.security import verify_password, CredentialException, createJWT
from core.schemas.users import User
from core.schemas.tokens import Token, TokenData, TokenUser
from utils.localization import _


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
    return Token(access_token=access_token, refresh_token=refresh_token, token_type=BEARER)