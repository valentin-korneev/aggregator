from logging import getLogger
from app.core.configs.general import GeneralConfig


config = GeneralConfig()
logger = getLogger(config.application.NAME)