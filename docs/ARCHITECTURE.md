# Kimi CLI Architecture (DeepSeek TUI-aligned)

This repository now follows a 5-layer architecture:

1. **User Interface Layer**
   - `kimi_mcp_client/main.py`: argparse entrypoint, one-shot/serve/resume/yolo/plan routing.
   - `kimi_mcp_client/tui/`: rich + prompt_toolkit app state, streaming, approval, clipboard.

2. **Core Engine Layer**
   - `kimi_mcp_client/core/engine.py`: async agent loop, checkpointing, event bus.
   - `kimi_mcp_client/core/turn_loop.py`: streaming turn execution and tool dispatch loop.
   - `kimi_mcp_client/core/capacity_flow.py`: soft/hard token guardrails.
   - `kimi_mcp_client/core/events.py`, `session.py`, `turn.py`, `ops.py`: typed runtime models.

3. **Tool & Extension Layer**
   - `kimi_mcp_client/tools/`: registry/spec + shell/file/todo/tasks/github/plan/subagent/rlm/automation tools.
   - `kimi_mcp_client/hooks/lifecycle.py`: pre/post tool hook execution.
   - `kimi_mcp_client/skills/loader.py`: SKILL.md discovery across home/workspace paths.
   - `kimi_mcp_client/mcp/client.py`: wiring for existing 8 MCP servers.

4. **Runtime API + Task Management**
   - `kimi_mcp_client/runtime_api.py`: aiohttp HTTP/SSE runtime API.
   - `kimi_mcp_client/task_manager.py`: durable queue, worker pool, timelines.
   - `kimi_mcp_client/runtime_threads.py`: thread/turn/event persistence.

5. **LLM Layer**
   - `kimi_mcp_client/llm_client.py`: abstract client + retry.
   - `kimi_mcp_client/client.py`: async Kimi/OpenAI-compatible HTTP streaming client.
   - `kimi_mcp_client/models.py`: typed pydantic request/response models.

## LSP Integration

- `kimi_mcp_client/lsp/manager.py` performs lazy startup per file extension.
- Missing binaries degrade silently.
- Tool registry invokes LSP post-edit hook after `write_file`, `edit_file`, and `apply_patch`.
- Engine injects pending diagnostics into the next model turn.

## Runtime Durability

- Turn checkpoint: `~/.kimi/sessions/checkpoints/latest.json`
- Offline queue: `~/.kimi/sessions/checkpoints/offline_queue.json`
- Tasks: `~/.kimi/tasks/*.json`
- Threads: `~/.kimi/threads/*.json`

## Modes

- **Normal**: approvals/hooks/policies apply.
- **Plan mode**: edit tools blocked via registry guard.
- **YOLO mode**: no approval UI guard, optimized for autonomous runs.
- **One-shot**: single turn and exit via `--one-shot`.
