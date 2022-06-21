from pydantic import BaseSettings, root_validator
from logging import Formatter, basicConfig, getLogger, DEBUG, INFO
from app.core.configs.application import ApplicationConfig
from app.core.configs.basic import BasicConfig
from app.core.enums.environment import EnvironmentState
from app.utils.rotating import RotatingFileHandler


class LogggingConfig(BaseSettings):
    FILE_NAME: str | None
    FILE_MAX_SIZE: int | None
    FILE_COUNT: int | None
    ROLLOVER_WHEN: str | None
    ROLLOVER_INTERVAL: int | None
    FORMAT: str | None
    ENCODING: str | None
    LOGGERS: str | list[str]

    @root_validator
    def root(cls, values):
        for f, m in ApplicationConfig.__fields__.items():
            for v in values:
                if isinstance(values[v], str):
                    values[v] = values[v].replace(f'%{f}%', m.default)
        values['LOGGERS'] = [v.strip() for v in values['LOGGERS'].split(',')]
        return values

    def init(self):
        basicConfig(encoding=self.ENCODING)
        handler = RotatingFileHandler(
            self.FILE_NAME, when=self.ROLLOVER_WHEN,
            interval=self.ROLLOVER_INTERVAL, backupCount=self.FILE_COUNT,
            encoding='utf-8', maxBytes=self.FILE_MAX_SIZE
        )
        handler.setFormatter(Formatter(self.FORMAT))
        from app.core.config import config
        handler.setLevel(DEBUG if config.environment.STATE == EnvironmentState.DEVELOPMENT else INFO)
        for logger in self.LOGGERS:
            getLogger(logger).addHandler(handler)

    class Config(BasicConfig):
        env_prefix = 'LOG_'