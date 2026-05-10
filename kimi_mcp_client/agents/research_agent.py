from __future__ import annotations


class ResearchOrchestrator:
    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def research(self, topic: str) -> dict:
        if hasattr(self.mcp, "perplexity"):
            return await self.mcp.perplexity.research(topic)
        return {"topic": topic, "summary": "No Perplexity server configured"}
