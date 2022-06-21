from enum import Enum


class EnvironmentState(Enum):
    DEVELOPMENT = 'dev'
    STAGE       = 'stage'
    PRODUCTION  = 'prod'