from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select

from src.auth.csrf import validate_csrf
from src.auth.passwords import verify_password
from src.db.postgres.config import async_session_maker
from src.db.postgres.models import AdminUser


class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        validate_csrf(request, form.get("csrf_token", ""))

        username = (form.get("username") or "").strip()
        password = form.get("password") or ""

        async with async_session_maker() as session:
            res = await session.execute(
                select(AdminUser).where(
                    AdminUser.username == username,
                    AdminUser.is_active == True,
                )
            )
            admin = res.scalar_one_or_none()

            if not admin:
                return False

            if not verify_password(password, admin.password_hash):
                return False

            request.session["admin_user"] = admin.username
            return True

    async def logout(self, request: Request) -> bool:
        request.session.pop("admin_user", None)
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("admin_user"))
