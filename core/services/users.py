from typing import List
from fastapi import Request, Response
from core.schemas.users import User
from core.database import connection
from core.security import parseJWT


async def get_user(username: str) -> User:
    query = 'select * from acl_role where username = :username'
    user = await connection.fetch_one(query=query, values={'username': username})
    return User(**user) if user else None


async def get_user_from_token(req: Request, token: str) -> User:
    token_data = parseJWT(req, token)
    print(token_data)
    return await get_user(username=token_data.user.username)


async def check_assignment(user_id: int, scopes: List[str]) -> bool:
    query = 'select count(0) > 0 as result from v_acl_assignment where role_id = :user_id and key = :permission_key'
    for scope in scopes:
        data = await connection.fetch_one(query=query, values={'user_id': user_id, 'permission_key': scope})
        if data.result:
            return True
    return False


async def log_request(req: Request, resp: Response):
    print(req.state.request_time)
    await connection.execute(
        query='insert into acl_log(role_id, uri_path, request_time, status_code) values (:role_id, :uri_path, :request_time, :status_code)',
        values={'role_id': req.state.user.id, 'uri_path': req.scope['path'], 'request_time': req.state.request_time, 'status_code': resp.status_code}
        )