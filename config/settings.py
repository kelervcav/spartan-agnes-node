from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    TOKEN_URL: str
    SCHEME_NAME: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()