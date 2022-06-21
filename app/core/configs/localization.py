from pydantic import BaseSettings, root_validator
from json import load
from app.core.configs.basic import BasicConfig


class LocalizationConfig(BaseSettings):
    DEFAULT: str | None
    LANGUAGES: str | dict
    PATH: str | None

    @root_validator
    def root(cls, values):
        values['LANGUAGES'] = {v.strip(): {} for v in values['LANGUAGES'].split(',')}
        for lang in values['LANGUAGES']:
            try:
                filename = values['PATH'].replace('%LANGUAGE%', lang)
                with open(filename, 'r', encoding='utf-8') as file:
                    values['LANGUAGES'][lang] = load(file)
            except FileNotFoundError:
                raise Exception(f'Language "{lang}" from localization list not found')
        return values

    class Config(BasicConfig):
        env_prefix = 'LOCALE_'