from __future__ import annotations

from .models import ChatMessage


def compact_messages(messages: list[ChatMessage], keep_last: int = 20) -> list[ChatMessage]:
    if len(messages) <= keep_last:
        return messages
    head = [ChatMessage(role="system", content="Conversation compacted for context budget.")]
    return head + messages[-keep_last:]
