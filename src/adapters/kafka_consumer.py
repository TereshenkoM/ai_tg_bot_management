import json
import logging
from typing import Any, AsyncIterator

from aiokafka import AIOKafkaConsumer

from src.config import KafkaConsumerConfig

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, cfg: KafkaConsumerConfig, *, topic: str) -> None:
        self._cfg = cfg
        self._topic = topic
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        if self._consumer is not None:
            return
        self._consumer = AIOKafkaConsumer(
            self._topic,
            bootstrap_servers=self._cfg.bootstrap_servers,
            group_id=self._cfg.group_id,
            auto_offset_reset=self._cfg.auto_offset_reset,
            enable_auto_commit=self._cfg.enable_auto_commit,
        )
        await self._consumer.start()

    async def stop(self) -> None:
        if self._consumer is None:
            return
        await self._consumer.stop()
        self._consumer = None

    async def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        if self._consumer is None:
            raise RuntimeError("consumer не запущен")

        async for message in self._consumer:
            logger.info(f"Получено сообщение {message}")
            yield json.loads(message.value.decode("utf-8"))
