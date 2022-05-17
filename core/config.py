from logging import getLogger
from core.configs.general import GeneralConfig


config = GeneralConfig()
logger = getLogger(config.application.NAME)