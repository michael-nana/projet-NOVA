from pathlib import Path

from .. import config
from ..registry import tool


def _safe(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not any(p.is_relative_to(r) for r in config.ALLOWED_ROOTS):
        raise PermissionError("Chemin hors des dossiers autorisés.")
    return p


@tool(
    "files_list",
    "Liste le contenu d'un dossier (dossiers autorisés uniquement). "
    "Autorisés : " + "; ".join(str(r) for r in config.ALLOWED_ROOTS),
    {"type": "object", "properties": {"path": {"type": "string"}},
     "required": ["path"], "additionalProperties": False},
    level=0,
)
def files_list(path: str) -> str:
    p = _safe(path)
    if not p.is_dir():
        raise NotADirectoryError(f"Pas un dossier : {p}")
    lines = []
    for i, child in enumerate(sorted(p.iterdir())):
        if i >= 200:
            lines.append("... (liste tronquée à 200 éléments)")
            break
        kind = "dossier" if child.is_dir() else f"fichier {child.stat().st_size} o"
        lines.append(f"[{kind}] {child.name}")
    return "\n".join(lines) or "(dossier vide)"
