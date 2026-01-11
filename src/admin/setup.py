from typing import Callable
from fastapi import FastAPI
from sqladmin import Admin

from src.admin.views import AiModelsAdmin, ModelResponsesAdmin
from src.auth.admin_backend import AdminAuthBackend
from src.repositories.postgres.uow import PostgresUoW


def setup_admin(
    app: FastAPI,
    engine,
    session_secret: str,
    *,
    uow_factory: Callable[[], PostgresUoW],
) -> None:
    auth_backend = AdminAuthBackend(uow_factory=uow_factory, secret_key=session_secret)

    app.state.admin_auth = auth_backend

    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=auth_backend,
    )
    admin.add_view(AiModelsAdmin)
    admin.add_view(ModelResponsesAdmin)
