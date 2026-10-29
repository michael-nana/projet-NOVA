import asyncio
import uuid

from fastapi import WebSocket
from nova_protocol import AgentHello, ToolCall, ToolManifest, ToolResult


class AgentHub:
    """Connexion unique vers l'agent PC (multi-appareils plus tard)."""

    def __init__(self) -> None:
        self.ws: WebSocket | None = None
        self.device_id: str | None = None
        self.tools: dict[str, ToolManifest] = {}
        self._pending: dict[str, asyncio.Future[ToolResult]] = {}

    @property
    def connected(self) -> bool:
        return self.ws is not None

    def attach(self, ws: WebSocket, hello: AgentHello) -> None:
        self.ws, self.device_id = ws, hello.device_id
        self.tools = {t.name: t for t in hello.tools}

    def drop(self, ws: WebSocket) -> None:
        if self.ws is ws:
            self.ws, self.device_id, self.tools = None, None, {}
            for fut in self._pending.values():
                if not fut.done():
                    fut.set_exception(ConnectionError("Agent déconnecté"))

    def resolve(self, res: ToolResult) -> None:
        fut = self._pending.get(res.call_id)
        if fut and not fut.done():
            fut.set_result(res)

    async def call(self, tool: str, args: dict, timeout: float) -> ToolResult:
        if not self.ws:
            raise ConnectionError("Aucun agent connecté")
        call_id = uuid.uuid4().hex
        fut: asyncio.Future[ToolResult] = asyncio.get_running_loop().create_future()
        self._pending[call_id] = fut
        try:
            await self.ws.send_text(ToolCall(call_id=call_id, tool=tool, args=args).model_dump_json())
            return await asyncio.wait_for(fut, timeout)
        finally:
            self._pending.pop(call_id, None)
