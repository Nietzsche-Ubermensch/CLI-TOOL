import pytest

from kimi_mcp_client.tools.registry import ToolRegistry
from kimi_mcp_client.tools.spec import ToolResult, ToolSpec


@pytest.mark.asyncio
async def test_registry_dispatches_and_respects_plan_mode():
    registry = ToolRegistry()

    async def handler(args):
        return ToolResult(content=f"ok:{args['value']}")

    registry.register(
        ToolSpec(name="read_file", description="", input_schema={"type": "object"}),
        handler,
    )
    result = await registry.dispatch("read_file", {"value": "x"})
    assert result.content == "ok:x"

    registry.plan_mode = True
    registry.register(
        ToolSpec(name="write_file", description="", input_schema={"type": "object"}),
        handler,
    )
    blocked = await registry.dispatch("write_file", {"value": "y"})
    assert blocked.is_error is True
