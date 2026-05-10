from __future__ import annotations

import asyncio

from .spec import ToolResult


async def _run(cmd: str) -> ToolResult:
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    text = out.decode("utf-8", errors="ignore") + err.decode("utf-8", errors="ignore")
    return ToolResult(content=text.strip(), is_error=proc.returncode != 0)


async def git_status(args: dict) -> ToolResult:
    return await _run("git --no-pager status --short")


async def git_diff(args: dict) -> ToolResult:
    return await _run("git --no-pager diff")


async def git_log(args: dict) -> ToolResult:
    return await _run("git --no-pager log --oneline -n 20")


async def git_blame(args: dict) -> ToolResult:
    path = args.get("path")
    return await _run(f"git --no-pager blame {path}")


async def gh_issue_read(args: dict) -> ToolResult:
    return await _run(f"gh issue view {args.get('number')} --json number,title,body")


async def gh_pr_read(args: dict) -> ToolResult:
    return await _run(f"gh pr view {args.get('number')} --json number,title,body")


async def gh_guarded_comment(args: dict) -> ToolResult:
    if not args.get("confirm"):
        return ToolResult(content="confirmation required", is_error=True)
    return await _run(f"gh {args.get('target','issue')} comment {args.get('number')} --body {args.get('body')!r}")
