from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Event:
    type: str


@dataclass(slots=True)
class TurnStarted(Event):
    turn_id: str


@dataclass(slots=True)
class ToolCalled(Event):
    tool_name: str
    args: dict[str, Any]


@dataclass(slots=True)
class ToolResult(Event):
    tool_name: str
    result: Any


@dataclass(slots=True)
class TurnComplete(Event):
    turn_id: str
    content: str


@dataclass(slots=True)
class ErrorEvent(Event):
    message: str
