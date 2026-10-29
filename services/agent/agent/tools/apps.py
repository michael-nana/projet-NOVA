import subprocess

from ..registry import tool

# LISTE BLANCHE : seules ces applications peuvent être lancées. Ajoute les tiennes ici.
APPS = {
    "bloc-notes": "notepad.exe",
    "calculatrice": "calc.exe",
    "explorateur": "explorer.exe",
    "paint": "mspaint.exe",
}


@tool(
    "apps_open",
    "Ouvre une application autorisée sur le PC. Applications disponibles : " + ", ".join(APPS),
    {"type": "object", "properties": {"name": {"type": "string", "enum": list(APPS)}},
     "required": ["name"], "additionalProperties": False},
    level=1,
)
def apps_open(name: str) -> str:
    if name not in APPS:
        raise ValueError(f"Application non autorisée : {name}")
    subprocess.Popen([APPS[name]], shell=False)
    return f"Application ouverte : {name}"
