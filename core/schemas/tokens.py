from typing import List
from pydantic import BaseModel


class TokenUser(BaseModel):
    id: int
    username: str
    description: str | None


class TokenData(BaseModel):
    user: TokenUser
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefresh(BaseModel):
    refresh_token: str