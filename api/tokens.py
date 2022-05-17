from core.schemas.tokens import Token, TokenRefresh
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from core.services.tokens import authenticate_user, createToken
from core.services.users import get_user_from_token
from utils.localization import _


router = APIRouter(prefix='/token')


@router.post('/', response_model=Token)
async def login(r: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    return await createToken(r, user, scopes=form_data.scopes)


@router.post('/refresh', response_model=Token)
async def refresh_access_token(r: Request, refresh_token: TokenRefresh):
    user = await get_user_from_token(r, token=refresh_token.refresh_token)
    return await createToken(r, user)
