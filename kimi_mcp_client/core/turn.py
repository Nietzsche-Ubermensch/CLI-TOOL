from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Turn:
    turn_id: str
    prompt: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    response: str = ""
