from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AppState:
    messages: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)

    def on_event(self, event) -> None:
        if event.type == "turn_complete":
            self.messages.append(event.content)
        elif event.type == "tool_called":
            self.tools.append(event.tool_name)
