from __future__ import annotations

from ..sandbox.execpolicy import PermissionEngine
from ..task_manager import DurableTaskManager
from .automation import cancel_scheduled, list_scheduled, schedule_task
from .file import apply_patch, edit_file, glob_files, grep_files, read_file, write_file
from .github import gh_guarded_comment, gh_issue_read, gh_pr_read, git_blame, git_diff, git_log, git_status
from .plan import build_plan_tools
from .registry import ToolRegistry
from .rlm import rlm_exec
from .shell import shell_tool
from .spec import ToolSpec
from .subagent import agent_spawn
from .tasks import build_task_tools
from .todo import checklist_update, todo_read, todo_write


def _spec(name: str, description: str) -> ToolSpec:
    return ToolSpec(name=name, description=description, input_schema={"type": "object", "properties": {}})


def build_default_registry(hooks, lsp_manager) -> ToolRegistry:
    registry = ToolRegistry(hook_runner=hooks, lsp_manager=lsp_manager)
    permission = PermissionEngine()
    task_manager = DurableTaskManager()

    registry.register(_spec("shell", "Execute shell command"), lambda args: shell_tool(args, permission))
    registry.register(_spec("read_file", "Read file"), read_file)
    registry.register(_spec("write_file", "Write file"), write_file)
    registry.register(_spec("edit_file", "Edit file"), edit_file)
    registry.register(_spec("apply_patch", "Apply patch"), apply_patch)
    registry.register(_spec("glob_files", "Glob files"), glob_files)
    registry.register(_spec("grep_files", "Grep files"), grep_files)

    registry.register(_spec("todo_write", "Write todos"), todo_write)
    registry.register(_spec("todo_read", "Read todos"), todo_read)
    registry.register(_spec("checklist_update", "Update checklist"), checklist_update)

    for name, handler in build_task_tools(task_manager).items():
        registry.register(_spec(name, "Task manager tool"), handler)

    registry.register(_spec("git_status", "Git status"), git_status)
    registry.register(_spec("git_diff", "Git diff"), git_diff)
    registry.register(_spec("git_log", "Git log"), git_log)
    registry.register(_spec("git_blame", "Git blame"), git_blame)
    registry.register(_spec("gh_issue_read", "Read GH issue"), gh_issue_read)
    registry.register(_spec("gh_pr_read", "Read GH PR"), gh_pr_read)
    registry.register(_spec("gh_guarded_comment", "Guarded GH comment"), gh_guarded_comment)

    registry.register(_spec("agent_spawn", "Spawn subagent"), agent_spawn)
    registry.register(_spec("rlm_exec", "Run sandboxed RLM code"), lambda args: rlm_exec(args))

    registry.register(_spec("schedule_task", "Schedule task"), schedule_task)
    registry.register(_spec("list_scheduled", "List schedules"), list_scheduled)
    registry.register(_spec("cancel_scheduled", "Cancel schedule"), cancel_scheduled)

    # Plan tools are engine-bound; attached by engine after init where needed.
    return registry
