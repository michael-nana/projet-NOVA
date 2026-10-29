import os
import socket
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env")

SERVER_URL = os.getenv("NOVA_SERVER_URL", "ws://127.0.0.1:8000/ws/agent")
AGENT_TOKEN = os.getenv("NOVA_AGENT_TOKEN", "")
DEVICE_ID = os.getenv("NOVA_DEVICE_ID", socket.gethostname())
DATA_DIR = ROOT / "data"
ALLOWED_ROOTS = [
    Path(p).expanduser().resolve()
    for p in os.getenv("NOVA_ALLOWED_ROOTS", str(Path.home() / "Documents")).split(";")
    if p.strip()
]
