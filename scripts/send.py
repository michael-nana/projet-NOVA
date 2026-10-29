"""Envoie un ordre au serveur : python scripts/send.py "ouvre le bloc-notes" """
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
base = os.getenv("NOVA_API_URL", "http://127.0.0.1:8000")
headers = {"Authorization": f"Bearer {os.getenv('NOVA_USER_TOKEN', '')}"}

if len(sys.argv) < 2:
    print(httpx.get(f"{base}/status", headers=headers).json())
else:
    r = httpx.post(f"{base}/command", json={"text": " ".join(sys.argv[1:])}, headers=headers, timeout=120)
    print(r.json())
