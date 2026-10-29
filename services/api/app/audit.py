"""Journal d'audit : une ligne JSON par événement (append-only)."""
import json
import time

from .config import settings


def log(event: str, **fields) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    line = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **fields}
    with open(settings.data_dir / "audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
