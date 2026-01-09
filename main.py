from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.admin.routes import admin_router
from src.admin.setup import setup_admin
from src.db.postgres.config import engine
from src.config import config
from logger import setup_logging, get_logger, RequestIdMiddleware

setup_logging(service_name="users-service")

log = get_logger(__name__)
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=config.SESSION_SECRET,
    same_site="lax",
    https_only=False if config.APP_ENV == "dev" else True,
)
app.add_middleware(RequestIdMiddleware)

app.include_router(admin_router)
setup_admin(app, engine, session_secret=config.SESSION_SECRET)
