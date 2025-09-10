from __future__ import annotations

from typing import AsyncGenerator, Dict, List

import asyncio

try:
  import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency
  genai = None

from .base import LLMClient


class GeminiClient(LLMClient):
  def __init__(self, api_key: str, model: str = "gemini-pro"):
    if genai is None:  # pragma: no cover - runtime guard
      raise RuntimeError("google-generativeai package is required")
    genai.configure(api_key=api_key)
    self.model = genai.GenerativeModel(model)

  async def stream_text(
    self,
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int,
  ) -> AsyncGenerator[str, None]:
    full_prompt = "\n".join([system_prompt] + [m["content"] for m in messages])
    stream = await asyncio.to_thread(
      self.model.generate_content,
      full_prompt,
      stream=True,
      generation_config={"max_output_tokens": max_tokens},
    )
    for chunk in stream:
      if chunk.text:
        yield chunk.text
