from __future__ import annotations

from .spec import ToolResult


def build_plan_tools(engine):
    async def plan_enter(args: dict) -> ToolResult:
        engine.set_plan_mode(True)
        return ToolResult(content="plan mode enabled")

    async def plan_exit(args: dict) -> ToolResult:
        engine.set_plan_mode(False)
        return ToolResult(content="plan mode disabled")

    return {"plan_enter": plan_enter, "plan_exit": plan_exit}
