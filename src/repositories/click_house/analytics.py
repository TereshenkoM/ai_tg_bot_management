from typing import Protocol


class AnalyticsRepository(Protocol):
    async def events_per_day(self, days: int) -> list[dict]: ...
