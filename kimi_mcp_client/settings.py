from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeSettings:
    model: str = "moonshot-v1-128k"
    provider: str = "kimi"
    base_url: str = "https://api.moonshot.cn/v1"
    lsp_enabled: bool = True
    yolo: bool = False
    plan_mode: bool = False
    max_workers: int = 2
