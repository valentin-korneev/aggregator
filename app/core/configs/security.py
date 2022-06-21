from pydantic import BaseSettings, SecretStr
from app.core.configs.basic import BasicConfig
from passlib.context import CryptContext


class SecurityConfig(BaseSettings):
    KEY: SecretStr | None
    ALGORITHM: str | None
    ACCESS_TOKEN_TTL: int | None
    REFRESH_TOKEN_TTL: int | None
    PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

    class Config(BasicConfig):
        env_prefix = 'SECURITY_'