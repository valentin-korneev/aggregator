from core.configs.application import ApplicationConfig
from core.configs.environment import EnvironmentConfig
from core.configs.localization import LocalizationConfig
from core.configs.logging import LogggingConfig
from core.configs.security import SecurityConfig
from core.configs.database import DatabaseConfig


class GeneralConfig():
    application: ApplicationConfig = ApplicationConfig()
    database: DatabaseConfig = DatabaseConfig()
    logging: LogggingConfig = LogggingConfig()
    environment: EnvironmentConfig = EnvironmentConfig()
    language: LocalizationConfig = LocalizationConfig()
    security: SecurityConfig = SecurityConfig()