import logging
import asyncio
from src.adapters.kafka_consumer import KafkaConsumer
from src.db.postgres.config import async_session_maker
from src.repositories.postgres.uow import PostgresUoW
from src.metrics import MetricsHub

logger = logging.getLogger(__name__)


async def consume_loop(consumer: KafkaConsumer, *, metrics_hub: MetricsHub | None = None) -> None:
    try:
        async for message in consumer:
            model = message.get("model")
            async with postgres_uow_factory() as uow:
                await uow.model_responses.add(message)
                await metrics_hub.ingest(kind="response", model=model)
    except Exception as e:
        logger.exception("consumer упал с ошибкой", exc_info=e)


def postgres_uow_factory() -> PostgresUoW:
    return PostgresUoW(async_session_maker)
