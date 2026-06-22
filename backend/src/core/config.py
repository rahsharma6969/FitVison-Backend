from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fitvision-api"
    app_env: str = "dev"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    database_url: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()