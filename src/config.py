from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    auth_jwt_secret: str
    auth_jwt_algorithm: str
    auth_jwt_secret_expiration: int
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()