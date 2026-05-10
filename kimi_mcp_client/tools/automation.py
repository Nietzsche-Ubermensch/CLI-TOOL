from __future__ import annotations

import json
import uuid
from pathlib import Path

from .spec import ToolResult

SCHEDULE_PATH = Path.home() / ".kimi" / "schedules.json"


def _load() -> dict:
    if SCHEDULE_PATH.exists():
        return json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
    return {"items": []}


def _save(data: dict) -> None:
    SCHEDULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEDULE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


async def schedule_task(args: dict) -> ToolResult:
    data = _load()
    item = {"id": str(uuid.uuid4()), "rrule": args.get("rrule"), "task": args.get("task")}
    data["items"].append(item)
    _save(data)
    return ToolResult(content=item["id"])


async def list_scheduled(args: dict) -> ToolResult:
    return ToolResult(content=json.dumps(_load(), indent=2))


async def cancel_scheduled(args: dict) -> ToolResult:
    data = _load()
    target = args.get("id")
    data["items"] = [item for item in data["items"] if item["id"] != target]
    _save(data)
    return ToolResult(content="canceled")
