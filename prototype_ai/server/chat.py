from __future__ import annotations

import os
from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from ..llm import create_client
from .switchable_stream import SwitchableStream

SYSTEM_PROMPT = "You are PrototypeAI, an expert AI assistant."
CONTINUE_PROMPT = (
  "Continue your prior response. IMPORTANT: Immediately begin from where you left off without any interruptions.\n"
  "Do not repeat any content, including artifact and action tags."
)
MAX_TOKENS = 4096
MAX_RESPONSE_SEGMENTS = 8

app = FastAPI()


def _client():
  provider = os.getenv("LLM_PROVIDER", "openai")
  if provider == "openai":
    return create_client(
      provider,
      api_key=os.environ["OPENAI_API_KEY"],
      model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    )
  if provider == "azure":
    return create_client(
      provider,
      api_key=os.environ["AZURE_OPENAI_API_KEY"],
      endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
      deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    )
  if provider == "gemini":
    return create_client(
      provider,
      api_key=os.environ["GEMINI_API_KEY"],
      model=os.getenv("GEMINI_MODEL", "gemini-pro"),
    )
  raise ValueError(f"Unknown provider: {provider}")


@app.post("/api/chat")
async def chat(request: Request):
  body = await request.json()
  messages: List[Dict[str, str]] = body["messages"]
  client = _client()
  stream = SwitchableStream()

  async def run():
    nonlocal messages
    for _ in range(MAX_RESPONSE_SEGMENTS):
      llm_stream = client.stream_text(messages, SYSTEM_PROMPT, MAX_TOKENS)
      await stream.switch(llm_stream)
      collected: List[str] = []
      async for token in stream:
        collected.append(token)
        yield token
      if len(collected) < MAX_TOKENS:
        break
      messages.append({"role": "assistant", "content": "".join(collected)})
      messages.append({"role": "user", "content": CONTINUE_PROMPT})

  return StreamingResponse(run(), media_type="text/plain")
