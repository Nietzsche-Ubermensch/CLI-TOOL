from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None


class LLMRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    stream: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMChunk(BaseModel):
    text: str = ""
    done: bool = False
    raw: Dict[str, Any] = Field(default_factory=dict)


class LLMResponse(BaseModel):
    content: str
    usage: Dict[str, Any] = Field(default_factory=dict)
    raw: Dict[str, Any] = Field(default_factory=dict)
