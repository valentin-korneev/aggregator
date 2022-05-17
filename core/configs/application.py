from pydantic import BaseModel


class ApplicationConfig(BaseModel):
    NAME: str = 'aggregator'
    VERSION: str = '0.0.1'