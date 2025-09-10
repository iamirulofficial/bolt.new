from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Optional


class SwitchableStream:
  def __init__(self):
    self._current: Optional[asyncio.Task] = None
    self._queue: asyncio.Queue[Optional[str]] = asyncio.Queue()
    self.switches = 0

  async def _pump(self, stream: AsyncGenerator[str, None]):
    try:
      async for token in stream:
        await self._queue.put(token)
    finally:
      await self._queue.put(None)

  async def switch(self, stream: AsyncGenerator[str, None]):
    if self._current:
      self._current.cancel()
    self._current = asyncio.create_task(self._pump(stream))
    self.switches += 1

  async def __aiter__(self):
    while True:
      token = await self._queue.get()
      if token is None:
        break
      yield token
