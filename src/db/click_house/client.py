import clickhouse_connect

from src.config import config

client = clickhouse_connect.get_async_client(
    host=config.CH_DB_HOST,
    port=config.CH_DB_PORT,
    username=config.CH_DB_USER,
    password=config.CH_DB_PASS,
    database=config.CH_DB_NAME,
)
