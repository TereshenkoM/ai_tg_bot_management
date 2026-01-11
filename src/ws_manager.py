from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any

from starlette.websockets import WebSocket


@dataclass(slots=True, frozen=True)
class WsMessage:
    type: str
    payload: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({"type": self.type, **self.payload}, ensure_ascii=False)


class WsManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast(self, message: WsMessage) -> None:
        data = message.to_json()
        async with self._lock:
            conns = list(self._connections)

        if not conns:
            return

        # рассылаем параллельно, ошибки отдельных соединений не валят всё
        async def _safe_send(conn: WebSocket) -> None:
            try:
                await conn.send_text(data)
            except Exception:
                await self.disconnect(conn)

        await asyncio.gather(*(_safe_send(c) for c in conns), return_exceptions=True)
