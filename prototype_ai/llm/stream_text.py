from __future__ import annotations

from typing import Awaitable, Callable, Dict, List, Optional

from .base import LLMClient
from .constants import MAX_TOKENS
from .factory import client_from_env
from .prompts import get_system_prompt

FinishCallback = Optional[Callable[[str, str], Awaitable[None]]]


def stream_text(
  messages: List[Dict[str, str]],
  client: Optional[LLMClient] = None,
  *,
  on_finish: FinishCallback = None,
):
  """Invoke the active LLM client and return its token stream."""
  if client is None:
    client = client_from_env()
  return client.stream_text(
    messages,
    get_system_prompt(),
    MAX_TOKENS,
    on_finish=on_finish,
  )
