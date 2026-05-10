import pytest

from kimi_mcp_client.hooks.lifecycle import HookConfig, HookRunner
from kimi_mcp_client.tools.spec import ToolResult


@pytest.mark.asyncio
async def test_pre_hook_allows_when_command_succeeds():
    runner = HookRunner([HookConfig(event="tool_call_before", command="true")])
    decision = await runner.run_pre("shell", {"command": "echo hi"})
    assert decision.allow is True


@pytest.mark.asyncio
async def test_pre_hook_blocks_on_failure():
    runner = HookRunner([HookConfig(event="tool_call_before", command="false")])
    decision = await runner.run_pre("shell", {})
    assert decision.allow is False


@pytest.mark.asyncio
async def test_post_hook_executes():
    runner = HookRunner([HookConfig(event="tool_call_after", command="true")])
    await runner.run_post("read_file", {}, ToolResult(content="ok"))
