import logging
import asyncio
from src.adapters.kafka_consumer import KafkaConsumer
from src.db.postgres.config import async_session_maker
from src.repositories.postgres.uow import PostgresUoW

logger = logging.getLogger(__name__)


async def consume_loop(consumer: KafkaConsumer) -> None:
    try:
        async for message in consumer:
            async with postgres_uow_factory() as uow:
                await uow.model_responses.add(message)
            logger.info("saved model response")
    except asyncio.CancelledError:
        logger.info("consumer loop cancelled")
        raise
    except Exception:
        logger.exception("consumer loop crashed")


def postgres_uow_factory() -> PostgresUoW:
    return PostgresUoW(async_session_maker)
