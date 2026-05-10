from __future__ import annotations

import fnmatch
import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path


class Action(Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


@dataclass(slots=True)
class Rule:
    permission: str
    pattern: str
    action: Action


class PermissionEngine:
    def __init__(self, *, path: Path | None = None):
        self.rules: list[Rule] = []
        self.path = path or (Path.home() / ".kimi" / "permissions.json")

    def evaluate(self, tool: str, path: str | None) -> Action:
        target = path or ""
        for rule in self.rules:
            if rule.permission not in (tool, "*"):
                continue
            if fnmatch.fnmatch(target, rule.pattern):
                return rule.action
        return Action.ALLOW

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(
                [{"permission": r.permission, "pattern": r.pattern, "action": r.action.value} for r in self.rules],
                indent=2,
            ),
            encoding="utf-8",
        )
