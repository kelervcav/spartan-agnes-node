from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Spartan"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
