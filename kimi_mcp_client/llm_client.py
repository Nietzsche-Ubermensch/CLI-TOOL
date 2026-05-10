from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import AsyncIterator

from .models import LLMChunk, LLMRequest, LLMResponse


class AbstractLLMClient(ABC):
    @abstractmethod
    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMChunk]:
        raise NotImplementedError

    async def complete(self, request: LLMRequest) -> LLMResponse:
        chunks: list[str] = []
        async for chunk in self.stream(request):
            if chunk.text:
                chunks.append(chunk.text)
        return LLMResponse(content="".join(chunks))


async def with_retry(
    operation,
    *,
    retries: int = 2,
    initial_backoff: float = 0.25,
):
    last_error = None
    for attempt in range(retries + 1):
        try:
            return await operation()
        except Exception as exc:  # pragma: no cover - generic retry wrapper
            last_error = exc
            if attempt == retries:
                raise
            await asyncio.sleep(initial_backoff * (2**attempt))
    raise last_error
