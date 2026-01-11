from __future__ import annotations

import asyncio
import time
from collections import Counter, deque
from dataclasses import dataclass
from typing import Any

from src.ws_manager import WsManager, WsMessage


@dataclass(slots=True)
class Event:
    ts: float
    kind: str
    model: str | None = None


class MetricsHub:
    def __init__(self, ws: WsManager, *, push_interval_sec: float = 1.0) -> None:
        self._ws = ws
        self._push_interval = push_interval_sec

        self._events_30s: deque[Event] = deque()
        self._events_5m: deque[Event] = deque()

        self._total = Counter()
        self._models_5m = Counter()

        self._stop = asyncio.Event()
        self._task: asyncio.Task[None] | None = None
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        if self._task:
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._run_push_loop())

    async def stop(self) -> None:
        self._stop.set()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except Exception:
                pass
            self._task = None

    async def ingest(self, *, kind: str, model: str | None = None, ts: float | None = None) -> None:
        now = ts if ts is not None else time.time()
        e = Event(ts=now, kind=kind, model=model)

        async with self._lock:
            if kind == "message":
                self._total["messages_total"] += 1
            elif kind == "response":
                self._total["responses_total"] += 1
            elif kind == "error":
                self._total["errors_total"] += 1

            self._events_30s.append(e)
            self._events_5m.append(e)
            if model:
                self._models_5m[model] += 1

            self._trim_locked(now)

    def _trim_locked(self, now: float) -> None:
        while self._events_30s and (now - self._events_30s[0].ts) > 30.0:
            self._events_30s.popleft()

        while self._events_5m and (now - self._events_5m[0].ts) > 300.0:
            old = self._events_5m.popleft()
            if old.model:
                self._models_5m[old.model] -= 1
                if self._models_5m[old.model] <= 0:
                    del self._models_5m[old.model]

    async def _run_push_loop(self) -> None:
        while not self._stop.is_set():
            await asyncio.sleep(self._push_interval)
            snapshot = await self.snapshot()
            await self._ws.broadcast(WsMessage(type="metrics", payload=snapshot))

    async def snapshot(self) -> dict[str, Any]:
        now = time.time()
        async with self._lock:
            self._trim_locked(now)

            c30 = Counter(e.kind for e in self._events_30s)
            rps = {
                "messages": round(c30.get("message", 0) / 30.0, 3),
                "responses": round(c30.get("response", 0) / 30.0, 3),
                "errors": round(c30.get("error", 0) / 30.0, 3),
            }

            top_models = self._models_5m.most_common(10)

            return {
                "ts": int(now),
                "counters": dict(self._total),
                "rps_30s": rps,
                "top_models_5m": top_models,
            }
