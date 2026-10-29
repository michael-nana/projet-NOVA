from dataclasses import dataclass
from typing import Any, Callable

from nova_protocol import ToolManifest


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    level: int
    fn: Callable[..., str]


REGISTRY: dict[str, Tool] = {}


def tool(name: str, description: str, schema: dict[str, Any] | None = None, level: int = 0):
    """Enregistre un outil. Un nouvel outil = une fonction décorée dans agent/tools/."""
    def deco(fn: Callable[..., str]):
        REGISTRY[name] = Tool(
            name, description,
            schema or {"type": "object", "properties": {}, "additionalProperties": False},
            level, fn,
        )
        return fn
    return deco


def manifests() -> list[ToolManifest]:
    return [ToolManifest(name=t.name, description=t.description,
                         input_schema=t.input_schema, level=t.level)  # type: ignore[arg-type]
            for t in REGISTRY.values()]
