import logging

from src.adapters.kafka_consumer import KafkaConsumer
from src.db.postgres.config import async_session_maker
from src.repositories.postgres.uow import PostgresUoW

logger = logging.getLogger(__name__)


async def consume_loop(consumer: KafkaConsumer) -> None:
    try:
        async for message in consumer:
            logger.info(message)
    except Exception:
        logger.exception("consumer loop stopped with error")


def postgres_uow_factory() -> PostgresUoW:
    return PostgresUoW(async_session_maker)
