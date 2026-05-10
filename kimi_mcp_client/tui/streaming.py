from __future__ import annotations


class StreamingCollector:
    def __init__(self):
        self.buffer: list[str] = []

    def append(self, token: str) -> None:
        self.buffer.append(token)

    def text(self) -> str:
        return "".join(self.buffer)
