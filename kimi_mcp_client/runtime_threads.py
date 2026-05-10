from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RuntimeThreadStore:
    schema_version = 1

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or (Path.home() / ".kimi" / "threads")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _thread_file(self, thread_id: str) -> Path:
        return self.base_dir / f"{thread_id}.json"

    def create_thread(self) -> dict[str, Any]:
        import uuid

        thread_id = str(uuid.uuid4())
        record = {"schema_version": self.schema_version, "id": thread_id, "turns": [], "events": []}
        self._thread_file(thread_id).write_text(json.dumps(record, indent=2), encoding="utf-8")
        return record

    def append_turn(self, thread_id: str, turn: Any) -> None:
        thread_file = self._thread_file(thread_id)
        if thread_file.exists():
            record = self.get_thread(thread_id)
        else:
            record = {"schema_version": self.schema_version, "id": thread_id, "turns": [], "events": []}
        record["turns"].append(turn.__dict__)
        thread_file.write_text(json.dumps(record, indent=2), encoding="utf-8")

    def append_event(self, thread_id: str, event: dict[str, Any]) -> None:
        record = self.get_thread(thread_id)
        record["events"].append(event)
        self._thread_file(thread_id).write_text(json.dumps(record, indent=2), encoding="utf-8")

    def get_thread(self, thread_id: str) -> dict[str, Any]:
        data = json.loads(self._thread_file(thread_id).read_text(encoding="utf-8"))
        if data.get("schema_version", 0) > self.schema_version:
            raise ValueError("Unsupported schema_version")
        return data
