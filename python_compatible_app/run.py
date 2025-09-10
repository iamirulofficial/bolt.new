from __future__ import annotations

import json
import sys

import requests

from .actions import apply_actions, parse_actions
from .diff import DiffTracker

SERVER_URL = "http://localhost:8000/api/chat"


def main() -> None:
  workdir = "."
  tracker = DiffTracker(workdir)
  history = []
  print("PrototypeAI interactive client. Type your prompt and press Enter.")
  while True:
    try:
      user_input = input("prompt> ")
    except EOFError:
      break
    if not user_input.strip():
      continue

    if tracker.snapshot:
      user_msg = f"{tracker.build_tag()}\n{user_input}"
    else:
      user_msg = user_input

    history.append({"role": "user", "content": user_msg})
    resp = requests.post(SERVER_URL, json={"messages": history}, stream=True)
    text = "".join(chunk.decode() for chunk in resp.iter_content(chunk_size=None))
    history.append({"role": "assistant", "content": text})

    actions = parse_actions(text)
    if actions:
      apply_actions(actions, workdir)
      tracker.take_snapshot()

    print(text)


if __name__ == "__main__":
  main()
