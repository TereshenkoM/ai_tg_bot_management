from src.auth.passwords import hash_password
from src.db.postgres.models import AdminUser


class AdminUserService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    async def create_admin(self, username: str, password: str) -> AdminUser:
        username = username.strip()
        if not username:
            raise ValueError("username пустой")
        if not password:
            raise ValueError("password пустой")

        async with self._uow_factory() as uow:
            assert uow.admin_users is not None

            exists = await uow.admin_users.get_by_username(username)
            if exists:
                raise RuntimeError(f"Пользователь '{username}' уже существует")

            user = AdminUser(
                username=username,
                password_hash=hash_password(password),
                is_active=True,
            )
            await uow.admin_users.create(user)
            return user
