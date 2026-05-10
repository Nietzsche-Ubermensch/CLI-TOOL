from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SubAgent:
    name: str
    task: str


class LaborMarket:
    async def spawn(self, name: str, task: str) -> SubAgent:
        return SubAgent(name=name, task=task)
