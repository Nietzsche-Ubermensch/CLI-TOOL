from __future__ import annotations


def estimate_cost_usd(prompt_tokens: int, completion_tokens: int, per_token_cost: float = 0.000002) -> float:
    return (prompt_tokens + completion_tokens) * per_token_cost
