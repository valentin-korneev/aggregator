from pydantic import BaseSettings, root_validator, SecretStr
from core.configs.basic import BasicConfig


class DatabaseConfig(BaseSettings):
    SCHEME: str | None
    USERNAME: str | None
    PASSWORD: SecretStr | None
    HOST: str | None
    PORT: int | None
    DBNAME: str | None
    DSN: str | None
    POOL_SIZE: int | None
    POOL_MAX_SIZE: int | None

    @root_validator
    def root(cls, values):
        values['DSN'] = '%s://%s:%s@%s:%s/%s' % (
            values['SCHEME'],
            values['USERNAME'],
            values['PASSWORD'].get_secret_value(),
            values['HOST'],
            values['PORT'],
            values['DBNAME']
        )
        return values

    class Config(BasicConfig):
        env_prefix = 'DATABASE_'