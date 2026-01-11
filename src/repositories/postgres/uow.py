from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.repositories.postgres.admin_users_repo import PgAdminUserRepository


class PostgresUoW:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker
        self.session: AsyncSession | None = None
        self.admin_users: PgAdminUserRepository | None = None

    async def __aenter__(self):
        self.session = self._session_maker()
        self.admin_users = PgAdminUserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        assert self.session is not None
        try:
            if exc is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        finally:
            await self.session.close()
