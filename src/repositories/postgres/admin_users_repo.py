from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.models import AdminUser
from src.repositories.postgres.admin_users import AdminUserRepository


class PgAdminUserRepository(AdminUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> AdminUser | None:
        res = await self.session.execute(
            select(AdminUser).where(AdminUser.username == username)
        )
        return res.scalar_one_or_none()

    async def get_active_by_username(self, username: str) -> AdminUser | None:
        res = await self.session.execute(
            select(AdminUser).where(
                AdminUser.username == username,
                AdminUser.is_active == True,
            )
        )
        return res.scalar_one_or_none()

    async def create(self, user: AdminUser) -> AdminUser:
        self.session.add(user)
        await self.session.flush()
        return user
