from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from ..llm import (
  CONTINUE_PROMPT,
  MAX_RESPONSE_SEGMENTS,
  client_from_env,
  stream_text,
)
from .switchable_stream import SwitchableStream

app = FastAPI()


@app.post("/api/chat")
async def chat(request: Request):
  body = await request.json()
  messages: List[Dict[str, str]] = body["messages"]
  client = client_from_env()
  stream = SwitchableStream()

  async def handle_finish(content: str, finish_reason: str):
    if finish_reason != "length":
      await stream.close()
      return
    if stream.switches >= MAX_RESPONSE_SEGMENTS:
      raise RuntimeError("Cannot continue message: Maximum segments reached")
    messages.append({"role": "assistant", "content": content})
    messages.append({"role": "user", "content": CONTINUE_PROMPT})
    next_stream = stream_text(messages, client=client, on_finish=handle_finish)
    await stream.switch(next_stream)

  first_stream = stream_text(messages, client=client, on_finish=handle_finish)
  await stream.switch(first_stream)

  async def generator():
    async for token in stream:
      yield token

  return StreamingResponse(generator(), media_type="text/plain")
