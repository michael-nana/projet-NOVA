"""Agent PC : connexion SORTANTE vers le serveur, exécution des outils."""
import asyncio
import json
import logging

import websockets
from nova_protocol import AgentHello, ToolCall, ToolResult

from . import config, tools  # noqa: F401  (tools enregistre les outils)
from .registry import REGISTRY, manifests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("nova-agent")


async def handle(ws, raw: str) -> None:
    call = ToolCall.model_validate_json(raw)
    t = REGISTRY.get(call.tool)
    if t is None:
        res = ToolResult(call_id=call.call_id, ok=False, error=f"Outil inconnu : {call.tool}")
    else:
        try:
            out = await asyncio.to_thread(t.fn, **call.args)
            res = ToolResult(call_id=call.call_id, ok=True, output=str(out))
        except Exception as e:
            res = ToolResult(call_id=call.call_id, ok=False, error=f"{type(e).__name__}: {e}")
    log.info("outil %s -> %s", call.tool, "ok" if res.ok else res.error)
    await ws.send(res.model_dump_json())


async def run() -> None:
    if not config.AGENT_TOKEN:
        raise SystemExit("NOVA_AGENT_TOKEN manquant dans .env")
    delay = 1
    while True:
        try:
            async with websockets.connect(config.SERVER_URL, max_size=2**20) as ws:
                await ws.send(AgentHello(device_id=config.DEVICE_ID, token=config.AGENT_TOKEN,
                                         tools=manifests()).model_dump_json())
                log.info("connecté à %s avec %d outils", config.SERVER_URL, len(REGISTRY))
                delay = 1
                async for raw in ws:
                    asyncio.create_task(handle(ws, raw))
        except (OSError, websockets.ConnectionClosed) as e:
            log.warning("connexion perdue (%s), nouvel essai dans %ss", e, delay)
        await asyncio.sleep(delay)
        delay = min(delay * 2, 30)


if __name__ == "__main__":
    asyncio.run(run())
