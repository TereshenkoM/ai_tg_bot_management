from fastapi import FastAPI
from sqladmin import Admin
from src.auth.admin_backend import AdminAuthBackend
from src.admin.views import AiModelsAdmin


def setup_admin(app: FastAPI, engine, session_secret: str) -> None:
    auth_backend = AdminAuthBackend(secret_key=session_secret)
    app.state.admin_auth = auth_backend

    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=auth_backend,
    )
    admin.add_view(AiModelsAdmin)
