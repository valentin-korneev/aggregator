from pydantic import BaseSettings, root_validator, SecretStr
from app.core.configs.basic import BasicConfig
from cryptography.fernet import Fernet
from os import getenv


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
        '''
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        print(key)
            b'B8XBLJDiroM3N2nCBuUlzPL06AmfV4XkPJ5OKsPZbC4='
        cipher = Fernet(key)
        password = "thepassword".encode('utf-8')
        token = cipher.encrypt(password)
        print(token)
            b'gAAAAABe_TUP82q1zMR9SZw1LpawRLHjgNLdUOmW31RApwASzeo4qWSZ52ZBYpSrb1kUeXNFoX0tyhe7kWuudNs2Iy7vUwaY7Q=='
        '''
        key = b'sTbJSR88YHRXM1YbgsNkOYo0VTlsC71jxzEIOOaLPpw='

        values['DSN'] = '%s://%s:%s@%s:%s/%s' % (
            values['SCHEME'],
            values['USERNAME'],
            Fernet(key).decrypt(str.encode(values['PASSWORD'].get_secret_value())).decode('utf-8'),
            getenv('DATABASE_HOST', values['HOST']),
            values['PORT'],
            values['DBNAME']
        )
        return values

    class Config(BasicConfig):
        env_prefix = 'DATABASE_'