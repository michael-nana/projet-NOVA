import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("NOVA_MODEL", "claude-sonnet-5-5")
    agent_token: str = os.getenv("NOVA_AGENT_TOKEN", "")
    user_token: str = os.getenv("NOVA_USER_TOKEN", "")
    tool_timeout: float = float(os.getenv("NOVA_TOOL_TIMEOUT", "30"))
    data_dir: Path = ROOT / "data"


settings = Settings()


def validate() -> None:
    missing = [
        n for n, v in [
            ("ANTHROPIC_API_KEY", settings.anthropic_api_key),
            ("NOVA_AGENT_TOKEN", settings.agent_token),
            ("NOVA_USER_TOKEN", settings.user_token),
        ] if not v
    ]
    if missing:
        raise RuntimeError(f"Variables manquantes dans .env : {', '.join(missing)}")
    if len(settings.agent_token) < 24 or len(settings.user_token) < 24:
        raise RuntimeError("Les tokens doivent faire au moins 24 caractères.")
