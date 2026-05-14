# MCP Server Architecture

## Overview
The Kimi MCP client uses a modular, config-driven architecture based on the Model Context Protocol (MCP). It allows seamless integration with multiple external tools (Linear, Slack, Notion, Perplexity, GitHub, etc.) through a unified Python interface.

Servers are defined externally (via npx or Python) and orchestrated by the client.

## Core Components

### 1. Configuration (`mcp_config.json`)
- Central JSON file defining all MCP servers.
- Structure:
  ```json
  {
    "mcpServers": {
      "linear": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-linear"],
        "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
      },
      "slack": { ... },
      "notion": { ... }
    }
  }
  ```
- Supports environment variable substitution.
- Easy to extend by adding new server entries.

### 2. KimiMCPClient (client.py)
- Main orchestrator class.
- Loads config and manages server lifecycle.
- Provides dot-notation access: `client.linear.create_issue(...)`
- Key methods:
  - `initialize()`: Loads config and starts servers.
  - Lazy server instantiation via `_server_registry()`.
  - `execute_chain()` for sequential async operations.
  - Workflows via `client.workflows`.

### 3. BaseMCPServer (servers/base.py)
- Abstract base class for all servers.
- Responsibilities:
  - Config storage
  - Shared `aiohttp.ClientSession` management (lazy, with timeout)
  - Request metrics (`request_count`, `last_used`)
  - Abstract `health_check()` method (must be implemented by subclasses)
  - Resource cleanup via `close()`

### 4. Specific Server Implementations (servers/*.py)
- Each server (e.g., `LinearServer`, `SlackServer`) inherits from `BaseMCPServer`.
- Implements `health_check()`.
- Exposes domain-specific methods that interact with the underlying MCP server.
- Communication typically via stdio or HTTP depending on the MCP server implementation.

## Communication Flow
1. Client instantiated.
2. `await client.initialize()` → loads config → creates server instances → runs health checks.
3. Method calls routed through server classes to the external MCP process.
4. Results returned synchronously or via async patterns.

## Extending with New Servers (e.g., Slack, Notion)
1. Add entry to `mcp_config.json`.
2. Create `NewServer` class in `servers/new_server.py` inheriting `BaseMCPServer`.
3. Implement `health_check()`.
4. Register in `client.py` `_server_registry()`.
5. Expose via property if desired.
6. Update documentation and workflows.

## Key Benefits
- **Modularity**: Servers are independent and swappable.
- **Configurability**: No code changes needed to add tools.
- **Observability**: Built-in metrics and health checks.
- **Extensibility**: Clear pattern for new integrations.

This architecture enables efficient, maintainable multi-tool automation.