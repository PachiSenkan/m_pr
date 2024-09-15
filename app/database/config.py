from pydantic_settings import BaseSettings

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "mag_db"
DB_USER = "postgres"
DB_PASSWORD = "root"


class Settings(BaseSettings):
    """App settings."""

    project_name: str = "alchemist"
    debug: bool = False
    environment: str = "local"

    # Database
    database_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


settings = Settings()
