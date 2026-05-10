from __future__ import annotations


def approve_tool(tool_name: str, args: dict) -> str:
    answer = input(f"Approve tool {tool_name} {args}? [y/n/always]: ").strip().lower()
    if answer not in {"y", "n", "always"}:
        return "n"
    return answer
