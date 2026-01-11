from dataclasses import dataclass

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

    CSRF_SESSION_KEY: str = "csrf_token"
    SESSION_SECRET: str

    APP_ENV: str

    KAFKA_BOOTSTRAP_SERVERS: str
    TOPIC_MANAGEMENT_MESSAGES: str
    KAFKA_GROUP_ID: str

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.PG_DB_USER}:{self.PG_DB_PASS}@{self.PG_DB_HOST}:{self.PG_DB_PORT}/{self.PG_DB_NAME}"

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


@dataclass(frozen=True, slots=True)
class KafkaConsumerConfig:
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True


config = Config()
