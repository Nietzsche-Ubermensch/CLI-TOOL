from __future__ import annotations

import json
from pathlib import Path

from .spec import ToolResult

TODO_PATH = Path.home() / ".kimi" / "todo.json"


def _read() -> dict:
    if TODO_PATH.exists():
        return json.loads(TODO_PATH.read_text(encoding="utf-8"))
    return {"items": []}


def _write(data: dict) -> None:
    TODO_PATH.parent.mkdir(parents=True, exist_ok=True)
    TODO_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


async def todo_write(args: dict) -> ToolResult:
    data = _read()
    data["items"] = args.get("items", [])
    _write(data)
    return ToolResult(content="todo updated")


async def todo_read(args: dict) -> ToolResult:
    return ToolResult(content=json.dumps(_read(), indent=2))


async def checklist_update(args: dict) -> ToolResult:
    data = _read()
    index = int(args.get("index", -1))
    done = bool(args.get("done", True))
    if index < 0 or index >= len(data.get("items", [])):
        return ToolResult(content="invalid index", is_error=True)
    data["items"][index]["done"] = done
    _write(data)
    return ToolResult(content="checklist item updated")
