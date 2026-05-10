from __future__ import annotations

from .spec import ToolHandler, ToolResult, ToolSpec


class ToolRegistry:
    def __init__(self, hook_runner=None, lsp_manager=None):
        self.specs: dict[str, ToolSpec] = {}
        self.handlers: dict[str, ToolHandler] = {}
        self.hook_runner = hook_runner
        self.lsp_manager = lsp_manager
        self.plan_mode = False

    def register(self, spec: ToolSpec, handler: ToolHandler) -> None:
        self.specs[spec.name] = spec
        self.handlers[spec.name] = handler

    async def dispatch(self, name: str, args: dict) -> ToolResult:
        if self.plan_mode and name in {"write_file", "edit_file", "apply_patch"}:
            return ToolResult(content="Plan mode: edit tools are disabled", is_error=True)

        if name not in self.handlers:
            return ToolResult(content=f"Unknown tool: {name}", is_error=True)

        if self.hook_runner:
            decision = await self.hook_runner.run_pre(name, args)
            if not decision.allow:
                return ToolResult(content=decision.reason, is_error=True)

        result = await self.handlers[name](args)

        if self.hook_runner:
            await self.hook_runner.run_post(name, args, result)

        if self.lsp_manager and name in {"write_file", "edit_file", "apply_patch"} and not result.is_error:
            path = args.get("path")
            if path:
                await self.lsp_manager.run_post_edit_hook(path)

        return result
