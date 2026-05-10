from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CapacityGuardrails:
    soft_limit_tokens: int = 80_000
    hard_limit_tokens: int = 120_000

    def check(self, token_estimate: int) -> str:
        if token_estimate >= self.hard_limit_tokens:
            return "hard"
        if token_estimate >= self.soft_limit_tokens:
            return "soft"
        return "ok"
