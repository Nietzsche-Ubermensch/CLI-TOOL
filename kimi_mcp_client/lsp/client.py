from __future__ import annotations

import asyncio
import json
from typing import Any


class JsonRpcLspClient:
    def __init__(self, command: list[str]):
        self.command = command
        self.proc: asyncio.subprocess.Process | None = None
        self._id = 0

    async def start(self) -> bool:
        self.proc = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        return True

    async def request(self, method: str, params: dict[str, Any]) -> None:
        if not self.proc or not self.proc.stdin:
            return
        self._id += 1
        payload = json.dumps({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params})
        frame = f"Content-Length: {len(payload)}\r\n\r\n{payload}".encode("utf-8")
        self.proc.stdin.write(frame)
        await self.proc.stdin.drain()

    async def stop(self) -> None:
        if self.proc and self.proc.returncode is None:
            self.proc.terminate()
            await self.proc.wait()
