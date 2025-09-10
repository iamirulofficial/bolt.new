from __future__ import annotations

from typing import AsyncGenerator, Awaitable, Callable, Dict, List, Optional

try:
  from openai import AzureOpenAI
except Exception:  # pragma: no cover - optional dependency
  AzureOpenAI = None

from .base import LLMClient


class AzureOpenAIClient(LLMClient):
  def __init__(self, api_key: str, endpoint: str, deployment: str):
    if AzureOpenAI is None:  # pragma: no cover - runtime guard
      raise RuntimeError("openai package with AzureOpenAI is required")
    self.client = AzureOpenAI(
      api_key=api_key,
      api_version="2024-02-15-preview",
      azure_endpoint=endpoint,
    )
    self.deployment = deployment

  async def stream_text(
    self,
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int,
    on_finish: Optional[Callable[[str, str], Awaitable[None]]] = None,
  ) -> AsyncGenerator[str, None]:
    payload = [{"role": "system", "content": system_prompt}, *messages]
    response = await self.client.chat.completions.create(
      model=self.deployment,
      messages=payload,
      max_tokens=max_tokens,
      stream=True,
    )
    collected: List[str] = []
    finish_reason = "stop"
    async for chunk in response:
      choice = chunk.choices[0]
      token = choice.delta.get("content")
      if token:
        collected.append(token)
        yield token
      if getattr(choice, "finish_reason", None):
        finish_reason = choice.finish_reason
    if on_finish:
      await on_finish("".join(collected), finish_reason)
