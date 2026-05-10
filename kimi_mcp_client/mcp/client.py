from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..servers import (
    BraveSearchServer,
    ChromeDevToolsServer,
    Context7Server,
    FirecrawlServer,
    GitHubServer,
    LinearServer,
    PerplexityServer,
    PlaywrightServer,
)


class MCPClient:
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = config_path
        self._servers: dict[str, Any] = {}
        self._config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        p = Path(self.config_path)
        if not p.exists():
            return {"mcpServers": {}}
        return json.loads(p.read_text(encoding="utf-8"))

    async def initialize(self) -> dict[str, Any]:
        registry = {
            "perplexity": PerplexityServer,
            "linear": LinearServer,
            "github": GitHubServer,
            "brave": BraveSearchServer,
            "firecrawl": FirecrawlServer,
            "chrome": ChromeDevToolsServer,
            "playwright": PlaywrightServer,
            "context7": Context7Server,
        }
        status = {}
        cfg = self._config.get("mcpServers", {})
        for name, cls in registry.items():
            instance = cls(cfg.get(name, {}))
            self._servers[name] = instance
            status[name] = await instance.health_check()
        return status

    def __getattr__(self, item: str) -> Any:
        if item in self._servers:
            return self._servers[item]
        raise AttributeError(item)
