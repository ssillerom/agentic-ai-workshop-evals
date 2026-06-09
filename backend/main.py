from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse

from .agent import run_support_conversation
from .schemas import ChatRequest, ChatResponse, HealthResponse
from .settings import ROOT_DIR, get_settings, is_langfuse_configured
from .support_data import get_support_context

settings = get_settings()

app = FastAPI(title="Dad IT Support Agent")


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        provider="openai",
        tracing_configured=is_langfuse_configured(settings),
    )


@app.get("/api/support-context")
def support_context() -> dict:
    return get_support_context()


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return run_support_conversation(request)
    except Exception as exc:
        return PlainTextResponse(str(exc), status_code=400)


def _safe_dist_file(path: str) -> Path | None:
    dist_dir = ROOT_DIR / "dist"
    if not dist_dir.exists():
        return None

    requested = (dist_dir / path).resolve()
    if not requested.is_relative_to(dist_dir.resolve()):
        return None
    return requested if requested.is_file() else dist_dir / "index.html"


@app.get("/{path:path}", response_model=None)
def client_app(path: str):
    file_path = _safe_dist_file(path)
    if file_path is None:
        return {"ok": "Build the client with npm run build:client to serve the React app."}
    return FileResponse(file_path)
