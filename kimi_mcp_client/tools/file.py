from __future__ import annotations

import glob
import re
from pathlib import Path

from .spec import ToolResult


async def read_file(args: dict) -> ToolResult:
    path = Path(args["path"]) 
    return ToolResult(content=path.read_text(encoding="utf-8"))


async def write_file(args: dict) -> ToolResult:
    path = Path(args["path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(args.get("content", ""), encoding="utf-8")
    return ToolResult(content=f"Wrote {path}")


async def edit_file(args: dict) -> ToolResult:
    path = Path(args["path"])
    old = args.get("old", "")
    new = args.get("new", "")
    content = path.read_text(encoding="utf-8")
    if old not in content:
        return ToolResult(content="Target string not found", is_error=True)
    path.write_text(content.replace(old, new), encoding="utf-8")
    return ToolResult(content=f"Edited {path}")


async def apply_patch(args: dict) -> ToolResult:
    # Minimal compatibility: replace exact old_text with new_text
    path = Path(args["path"])
    old_text = args.get("old_text", "")
    new_text = args.get("new_text", "")
    content = path.read_text(encoding="utf-8")
    if old_text not in content:
        return ToolResult(content="Patch context not found", is_error=True)
    path.write_text(content.replace(old_text, new_text), encoding="utf-8")
    return ToolResult(content=f"Patched {path}")


async def glob_files(args: dict) -> ToolResult:
    pattern = args.get("pattern", "**/*")
    matches = glob.glob(pattern, recursive=True)
    return ToolResult(content="\n".join(matches))


async def grep_files(args: dict) -> ToolResult:
    pattern = args.get("pattern", "")
    path_pattern = args.get("paths", "**/*")
    regex = re.compile(pattern)
    hits: list[str] = []
    for candidate in glob.glob(path_pattern, recursive=True):
        p = Path(candidate)
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for idx, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                hits.append(f"{candidate}:{idx}:{line}")
    return ToolResult(content="\n".join(hits))
