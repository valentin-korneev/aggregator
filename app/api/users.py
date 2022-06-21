from fastapi import APIRouter, Request, Security
from app.core.dependecies import get_current_active_user
from app.core.schemas.users import User


router = APIRouter(prefix='/users')


@router.get('/me', response_model=User)
async def get_current_user(r: Request, current_user: User = Security(get_current_active_user, scopes=['users.me'])):
    return current_user