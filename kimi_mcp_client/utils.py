from __future__ import annotations

import hashlib
from pathlib import Path


def project_hash(path: str | Path) -> str:
    return hashlib.sha1(str(Path(path).resolve()).encode("utf-8")).hexdigest()[:12]
