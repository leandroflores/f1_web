from fastapi import Depends
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # db
    database_url: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


settings = Settings()


@lru_cache
def _get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(_get_settings)]
