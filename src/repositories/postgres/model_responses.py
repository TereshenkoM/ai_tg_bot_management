from typing import Any, Protocol
from src.db.postgres.models import ModelResponses

class ModelResponsesRepository(Protocol):
    async def add(self, data: dict[str, Any]) -> ModelResponses: ...
