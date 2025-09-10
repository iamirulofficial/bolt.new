from __future__ import annotations

import difflib
from pathlib import Path
from typing import Dict

TAG_NAME = "prototype_file_modifications"


class DiffTracker:
  def __init__(self, root: str):
    self.root = Path(root)
    self.snapshot: Dict[str, str] = {}
    self.take_snapshot()

  def take_snapshot(self) -> None:
    self.snapshot = {}
    for path in self.root.rglob('*'):
      if path.is_file():
        rel = path.relative_to(self.root).as_posix()
        self.snapshot[rel] = path.read_text(encoding='utf-8')

  def build_tag(self) -> str:
    parts = [f"<{TAG_NAME}>"]
    current: Dict[str, str] = {}
    for path in self.root.rglob('*'):
      if path.is_file():
        rel = path.relative_to(self.root).as_posix()
        current[rel] = path.read_text(encoding='utf-8')

    for rel, content in current.items():
      old = self.snapshot.get(rel)
      if old is None:
        parts.append(f"  <file path=\"{self.root / rel}\">{content}</file>")
      elif old != content:
        diff = '\n'.join(
          difflib.unified_diff(
            old.splitlines(), content.splitlines(), n=3, lineterm=''
          )
        )
        parts.append(f"  <diff path=\"{self.root / rel}\">{diff}</diff>")

    for rel in set(self.snapshot) - set(current):
      old = self.snapshot[rel]
      diff = '\n'.join(
        difflib.unified_diff(
          old.splitlines(), [], n=3, lineterm=''
        )
      )
      parts.append(f"  <diff path=\"{self.root / rel}\">{diff}</diff>")

    parts.append(f"</{TAG_NAME}>")
    return '\n'.join(parts)
