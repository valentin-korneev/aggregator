from pydantic import BaseModel


class User(BaseModel):
    id: int
    can_login: bool
    username: str | None
    description: str | None
    is_active: bool
    is_admin: bool
    hashed_password: str | None