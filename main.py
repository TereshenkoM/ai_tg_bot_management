import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from logger import RequestIdMiddleware, get_logger, setup_logging
from starlette.middleware.sessions import SessionMiddleware

from src.adapters.kafka_consumer import KafkaConsumer
from src.admin.routes import admin_router
from src.admin.setup import setup_admin
from src.config import KafkaConsumerConfig, config
from src.db.postgres.config import engine
from src.runtime import consume_loop

setup_logging(service_name="management")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = KafkaConsumer(
        KafkaConsumerConfig(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            group_id=config.KAFKA_GROUP_ID,
            enable_auto_commit=True,
        ),
        topic=config.TOPIC_MANAGEMENT_MESSAGES,
    )

    await consumer.start()
    logger.info("consumer запущен")

    consumer_task = asyncio.create_task(consume_loop(consumer))

    try:
        yield
    finally:
        if consumer_task:
            consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await consumer_task

        if consumer:
            await consumer.stop()
            logger.info("consumer остановлен")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.SESSION_SECRET,
    same_site="lax",
    https_only=False if config.APP_ENV == "dev" else True,
)
app.add_middleware(RequestIdMiddleware)

app.include_router(admin_router)
setup_admin(app, engine, session_secret=config.SESSION_SECRET)
