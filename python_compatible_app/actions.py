from __future__ import annotations

import os
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Action:
  kind: str  # 'file' or 'shell'
  file_path: str | None = None
  content: str | None = None
  command: str | None = None


def parse_actions(text: str) -> List[Action]:
  """Parse `<prototypeArtifact>` blocks from model output."""
  actions: List[Action] = []
  try:
    root = ET.fromstring(text)
  except ET.ParseError:
    return actions

  if root.tag != "prototypeArtifact":
    return actions

  for node in root.findall("prototypeAction"):
    kind = node.attrib.get("type")
    if kind == "file":
      path = node.attrib.get("filePath")
      content = node.text or ""
      actions.append(Action(kind="file", file_path=path, content=content))
    elif kind == "shell":
      cmd = node.text or ""
      actions.append(Action(kind="shell", command=cmd))
  return actions


def apply_actions(actions: Iterable[Action], workdir: str = ".") -> None:
  for action in actions:
    if action.kind == "file" and action.file_path is not None:
      target = Path(workdir, action.file_path)
      target.parent.mkdir(parents=True, exist_ok=True)
      target.write_text(action.content or "", encoding="utf-8")
    elif action.kind == "shell" and action.command is not None:
      subprocess.run(action.command, shell=True, cwd=workdir, check=False)
