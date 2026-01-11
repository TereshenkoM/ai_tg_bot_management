from __future__ import annotations

from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from src.auth.csrf import validate_csrf
from src.auth.passwords import verify_password


class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, uow_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._uow_factory = uow_factory

    async def login(self, request: Request) -> bool:
        form = await request.form()
        validate_csrf(request, form.get("csrf_token", ""))

        username = (form.get("username") or "").strip()
        password = form.get("password") or ""

        if not username or not password:
            return False

        async with self._uow_factory() as uow:
            admin = await uow.admin_users.get_active_by_username(username)
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
