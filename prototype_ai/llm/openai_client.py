from __future__ import annotations

from typing import AsyncGenerator, Dict, List

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
  ) -> AsyncGenerator[str, None]:
    payload = [{"role": "system", "content": system_prompt}, *messages]
    response = await openai.ChatCompletion.acreate(
      model=self.model,
      messages=payload,
      max_tokens=max_tokens,
      stream=True,
    )
    async for chunk in response:
      token = chunk["choices"][0]["delta"].get("content")
      if token:
        yield token
