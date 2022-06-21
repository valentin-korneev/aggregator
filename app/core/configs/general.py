from app.core.configs.application import ApplicationConfig
from app.core.configs.environment import EnvironmentConfig
from app.core.configs.localization import LocalizationConfig
from app.core.configs.logging import LogggingConfig
from app.core.configs.security import SecurityConfig
from app.core.configs.database import DatabaseConfig


class GeneralConfig():
    application: ApplicationConfig = ApplicationConfig()
    database: DatabaseConfig = DatabaseConfig()
    logging: LogggingConfig = LogggingConfig()
    environment: EnvironmentConfig = EnvironmentConfig()
    language: LocalizationConfig = LocalizationConfig()
    security: SecurityConfig = SecurityConfig()