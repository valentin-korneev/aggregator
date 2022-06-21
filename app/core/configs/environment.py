from pydantic import BaseSettings
from app.core.configs.basic import BasicConfig
from app.core.enums.environment import EnvironmentState


class EnvironmentConfig(BaseSettings):
    STATE: EnvironmentState | None

    class Config(BasicConfig):
        env_prefix = 'ENV_'