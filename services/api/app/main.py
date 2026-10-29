import asyncio
import hmac
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from nova_protocol import AgentHello, ToolResult
from pydantic import BaseModel, Field

from . import audit, config, llm
from .hub import AgentHub


@asynccontextmanager
async def lifespan(_: FastAPI):
    config.validate()
    yield


app = FastAPI(title="NOVA API", lifespan=lifespan)
hub = AgentHub()


def require_user(authorization: str = Header(default="")) -> None:
    token = authorization.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token, config.settings.user_token):
        raise HTTPException(status_code=401, detail="Non autorisé")


class CommandIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.get("/status", dependencies=[Depends(require_user)])
async def status():
    return {"agent_connected": hub.connected, "device": hub.device_id, "tools": sorted(hub.tools)}


@app.post("/command", dependencies=[Depends(require_user)])
async def command(body: CommandIn):
    audit.log("command", text=body.text)
    try:
        reply = await llm.run_command(body.text, hub)
    except Exception as e:
        audit.log("llm_error", error=str(e))
        raise HTTPException(status_code=502, detail=f"Erreur du cerveau IA : {e}")
    return {"reply": reply}


@app.websocket("/ws/agent")
async def ws_agent(ws: WebSocket):
    await ws.accept()
    try:
        hello = AgentHello.model_validate_json(await asyncio.wait_for(ws.receive_text(), 10))
    except Exception:
        await ws.close(code=1008)
        return
    if not hmac.compare_digest(hello.token, config.settings.agent_token):
        audit.log("agent_rejected", device=hello.device_id)
        await ws.close(code=1008)
        return
    hub.attach(ws, hello)
    audit.log("agent_connected", device=hello.device_id, tools=[t.name for t in hello.tools])
    try:
        while True:
            hub.resolve(ToolResult.model_validate_json(await ws.receive_text()))
    except WebSocketDisconnect:
        pass
    finally:
        hub.drop(ws)
        audit.log("agent_disconnected", device=hello.device_id)
