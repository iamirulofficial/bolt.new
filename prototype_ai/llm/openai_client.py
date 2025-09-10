from __future__ import annotations

from typing import AsyncGenerator, Awaitable, Callable, Dict, List, Optional

import asyncio

try:
  import openai
except Exception:  # pragma: no cover - optional dependency
  openai = None

from .base import LLMClient


class OpenAIClient(LLMClient):
  def __init__(self, api_key: str, model: str):
    if openai is None:  # pragma: no cover - runtime guard
      raise RuntimeError("openai package is required")
    openai.api_key = api_key
    self.model = model

  async def stream_text(
    self,
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int,
    on_finish: Optional[Callable[[str, str], Awaitable[None]]] = None,
  ) -> AsyncGenerator[str, None]:
    payload = [{"role": "system", "content": system_prompt}, *messages]
    response = await openai.ChatCompletion.acreate(
      model=self.model,
      messages=payload,
      max_tokens=max_tokens,
      stream=True,
    )
    collected: List[str] = []
    finish_reason = "stop"
    async for chunk in response:
      choice = chunk["choices"][0]
      token = choice["delta"].get("content")
      if token:
        collected.append(token)
        yield token
      if choice.get("finish_reason"):
        finish_reason = choice["finish_reason"]
    if on_finish:
      await on_finish("".join(collected), finish_reason)
