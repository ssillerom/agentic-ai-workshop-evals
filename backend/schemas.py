from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ChatRole = Literal["user", "assistant"]


class ChatMessage(BaseModel):
    id: str = Field(min_length=1)
    role: ChatRole
    content: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    messages: list[ChatMessage] = Field(min_length=1)
    session_id: str = Field(alias="sessionId", min_length=1)
    user_id: str | None = Field(default=None, alias="userId")


class TraceMeta(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    context_id: str = Field(alias="contextId")
    context_label: str = Field(alias="contextLabel")
    model: str


class ChatResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    answer: str
    used_tools: list[str] = Field(alias="usedTools")
    trace_meta: TraceMeta = Field(alias="traceMeta")


class HealthResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ok: bool
    provider: str
    tracing_configured: bool = Field(alias="tracingConfigured")
