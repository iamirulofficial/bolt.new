from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List


class LLMClient(ABC):
  @abstractmethod
  async def stream_text(
    self,
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int,
  ) -> AsyncGenerator[str, None]:
    """Yield tokens for the given conversation."""
    raise NotImplementedError
