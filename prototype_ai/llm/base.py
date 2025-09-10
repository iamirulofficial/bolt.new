from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Awaitable, Callable, Dict, List, Optional


class LLMClient(ABC):
  @abstractmethod
  async def stream_text(
    self,
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int,
    on_finish: Optional[Callable[[str, str], Awaitable[None]]] = None,
  ) -> AsyncGenerator[str, None]:
    """Yield tokens for the given conversation."""
    raise NotImplementedError
