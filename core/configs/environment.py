from pydantic import BaseSettings
from core.configs.basic import BasicConfig
from core.enums.environment import EnvironmentState


class EnvironmentConfig(BaseSettings):
    STATE: EnvironmentState | None

    class Config(BasicConfig):
        env_prefix = 'ENV_'