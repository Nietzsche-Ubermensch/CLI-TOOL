import pytest

from kimi_mcp_client.lsp.manager import LspManager


@pytest.mark.asyncio
async def test_lsp_manager_silent_when_binary_missing(tmp_path):
    manager = LspManager(enabled=True)
    file_path = tmp_path / "a.unknown"
    file_path.write_text("hi", encoding="utf-8")
    await manager.run_post_edit_hook(str(file_path))
    assert manager.pop_pending_messages() == []
