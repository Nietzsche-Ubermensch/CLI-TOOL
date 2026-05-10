import pytest

from kimi_mcp_client.config import LoadedConfig
from kimi_mcp_client.core.engine import AgentEngine
from kimi_mcp_client.hooks.lifecycle import HookConfig
from kimi_mcp_client.models import LLMChunk
from kimi_mcp_client.settings import RuntimeSettings


class StubLLM:
    async def stream(self, request):
        yield LLMChunk(text="hello world")


@pytest.mark.asyncio
async def test_engine_one_turn_emits_completion():
    cfg = LoadedConfig(raw={}, settings=RuntimeSettings(), hooks=[HookConfig(event="tool_call_before", command="true")], permission_rules={})
    engine = AgentEngine(settings=RuntimeSettings(), llm_client=StubLLM(), config=cfg)
    content = await engine.handle_prompt("hi")
    assert "hello world" in content
