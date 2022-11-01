import logging

from pydantic import BaseSettings, Field


logging.basicConfig(
    level=logging.INFO,

    format="{asctime} {levelname}:{name} — {filename}: {message}",
    datefmt="%d.%m.%Y %H:%M:%S",
    style="{",
)


class Settings(BaseSettings):
    token: str = Field(..., env="BOT_TOKEN")
    credentials: dict = Field(..., env="SERVICE_ACCOUNT_CREDENTIALS")

    root: str = Field(..., env="PATH_TO_ROOT_FOLDER")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
