from __future__ import annotations

import uuid

from .spec import ToolResult


async def agent_spawn(args: dict) -> ToolResult:
    return ToolResult(content=str(uuid.uuid4()), metadata={"task": args.get("task", "")})
