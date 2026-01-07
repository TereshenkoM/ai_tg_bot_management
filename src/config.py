from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    PG_DB_HOST: str
    PG_DB_PORT: int
    PG_DB_USER: str
    PG_DB_PASS: str
    PG_DB_NAME: str

    CH_DB_HOST: str
    CH_DB_PORT: int
    CH_DB_USER: str
    CH_DB_PASS: str
    CH_DB_NAME: str

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.PG_DB_USER}:{self.PG_DB_PASS}@{self.PG_DB_HOST}:{self.PG_DB_PORT}/{self.PG_DB_NAME}"

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Config()
