import asyncio
import logging

from src.adapters.kafka_consumer import KafkaConsumer

logger = logging.getLogger(__name__)


async def consume_loop(consumer: KafkaConsumer):
    try:
        async for message in consumer:
            logger.info(message)
    except Exception:
        logger.exception("consumer остановлен")
