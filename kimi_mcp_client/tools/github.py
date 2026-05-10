from __future__ import annotations

import asyncio

from .spec import ToolResult


async def _run(argv: list[str]) -> ToolResult:
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    text = out.decode("utf-8", errors="ignore") + err.decode("utf-8", errors="ignore")
    return ToolResult(content=text.strip(), is_error=proc.returncode != 0)


async def git_status(args: dict) -> ToolResult:
    return await _run(["git", "--no-pager", "status", "--short"])


async def git_diff(args: dict) -> ToolResult:
    return await _run(["git", "--no-pager", "diff"])


async def git_log(args: dict) -> ToolResult:
    return await _run(["git", "--no-pager", "log", "--oneline", "-n", "20"])


async def git_blame(args: dict) -> ToolResult:
    path = args.get("path")
    if not path:
        return ToolResult(content="Missing required argument: path", is_error=True)
    return await _run(["git", "--no-pager", "blame", path])


async def gh_issue_read(args: dict) -> ToolResult:
    number = str(args.get("number", ""))
    return await _run(["gh", "issue", "view", number, "--json", "number,title,body"])


async def gh_pr_read(args: dict) -> ToolResult:
    number = str(args.get("number", ""))
    return await _run(["gh", "pr", "view", number, "--json", "number,title,body"])


async def gh_guarded_comment(args: dict) -> ToolResult:
    if not args.get("confirm"):
        return ToolResult(content="confirmation required", is_error=True)
    target = args.get("target", "issue")
    number = str(args.get("number", ""))
    body = str(args.get("body", ""))
    return await _run(["gh", target, "comment", number, "--body", body])
