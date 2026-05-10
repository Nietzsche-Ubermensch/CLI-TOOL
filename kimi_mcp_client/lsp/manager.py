from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from .client import JsonRpcLspClient
from .diagnostics import Diagnostic, render_diagnostics
from .registry import EXTENSION_TO_SERVER


class LspManager:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.clients: dict[str, JsonRpcLspClient] = {}
        self._pending_messages: list[str] = []

    async def _ensure_client(self, file_path: str) -> JsonRpcLspClient | None:
        if not self.enabled:
            return None
        ext = Path(file_path).suffix
        command = EXTENSION_TO_SERVER.get(ext)
        if not command:
            return None
        binary = command[0]
        if shutil.which(binary) is None:
            return None
        key = " ".join(command)
        if key not in self.clients:
            client = JsonRpcLspClient(command)
            await client.start()
            self.clients[key] = client
        return self.clients[key]

    async def run_post_edit_hook(self, file_path: str) -> None:
        client = await self._ensure_client(file_path)
        if client is None:
            return
        text = await asyncio.to_thread(Path(file_path).read_text, encoding="utf-8")
        await client.request("textDocument/didOpen", {"textDocument": {"uri": f"file://{file_path}", "languageId": "text", "version": 1, "text": text}})

    def add_diagnostics(self, diags: list[Diagnostic]) -> None:
        rendered = render_diagnostics(diags)
        if rendered:
            self._pending_messages.append(rendered)

    def pop_pending_messages(self) -> list[str]:
        out = self._pending_messages[:]
        self._pending_messages.clear()
        return out
