from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.models import ModelResponses


class PgModelResponsesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict[str, Any]) -> ModelResponses:
        row = ModelResponses(data=data)
        self.session.add(row)
        await self.session.flush()
        return row
