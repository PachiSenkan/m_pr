from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# DB_HOST = "localhost"
# DB_PORT = 5432
# DB_NAME = "mag_db"
# DB_USER = "postgres"
# DB_PASSWORD = "root"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="allow")
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    project_name: str = "mag"
    debug: bool = False
    environment: str = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
