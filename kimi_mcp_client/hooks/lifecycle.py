from __future__ import annotations

import asyncio
import os
import re
from dataclasses import dataclass

from ..tools.spec import ToolResult


@dataclass(slots=True)
class HookConfig:
    event: str
    command: str
    matcher: str | None = None
    timeout_sec: int = 30


@dataclass(slots=True)
class HookDecision:
    allow: bool
    reason: str = ""


class HookRunner:
    def __init__(self, hooks: list[HookConfig] | None = None):
        self.hooks = hooks or []

    def _matches(self, hook: HookConfig, tool_name: str, event: str) -> bool:
        if hook.event != event:
            return False
        if not hook.matcher:
            return True
        return re.search(hook.matcher, tool_name) is not None

    async def _run_hook(self, hook: HookConfig, env: dict[str, str]) -> int:
        proc = await asyncio.create_subprocess_shell(hook.command, env=env)
        try:
            await asyncio.wait_for(proc.wait(), timeout=hook.timeout_sec)
        except TimeoutError:
            proc.kill()
            return 124
        return int(proc.returncode or 0)

    async def run_pre(self, tool_name: str, args: dict) -> HookDecision:
        env = {**os.environ, "TOOL_NAME": tool_name, "TOOL_ARGS": str(args)}
        for hook in self.hooks:
            if not self._matches(hook, tool_name, "tool_call_before"):
                continue
            rc = await self._run_hook(hook, env)
            if rc != 0:
                return HookDecision(allow=False, reason=f"FailedAbort: hook exit={rc}")
        return HookDecision(allow=True)

    async def run_post(self, tool_name: str, args: dict, result: ToolResult) -> None:
        env = {
            **os.environ,
            "TOOL_NAME": tool_name,
            "TOOL_ARGS": str(args),
            "TOOL_RESULT": result.content,
            "TOOL_ERROR": str(result.is_error).lower(),
        }
        for hook in self.hooks:
            if self._matches(hook, tool_name, "tool_call_after"):
                await self._run_hook(hook, env)
