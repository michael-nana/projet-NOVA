"""Langage commun entre le serveur (api) et l'agent PC."""
from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolManifest(BaseModel):
    name: str  # lettres, chiffres, _ et - uniquement (contrainte de l'API Claude)
    description: str
    input_schema: dict[str, Any]
    level: Literal[0, 1, 2, 3] = 3  # niveau de permission L0..L3


class AgentHello(BaseModel):
    type: Literal["hello"] = "hello"
    device_id: str
    token: str
    tools: list[ToolManifest]


class ToolCall(BaseModel):
    type: Literal["tool_call"] = "tool_call"
    call_id: str
    tool: str
    args: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    type: Literal["tool_result"] = "tool_result"
    call_id: str
    ok: bool
    output: str = ""
    error: str | None = None
