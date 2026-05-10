from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Diagnostic:
    file_path: str
    line: int
    column: int
    severity: int
    message: str
    source: str = "lsp"


def render_diagnostics(diags: list[Diagnostic]) -> str:
    rows = []
    for d in diags:
        rows.append(f"{d.file_path}:{d.line}:{d.column} [{d.severity}] {d.message} ({d.source})")
    return "\n".join(rows)
