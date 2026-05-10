from __future__ import annotations

from dataclasses import dataclass, field

from .turn import Turn


@dataclass
class SessionState:
    session_id: str
    plan_mode: bool = False
    turns: list[Turn] = field(default_factory=list)
    pending_diagnostics: list[str] = field(default_factory=list)
