from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Spartan"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
