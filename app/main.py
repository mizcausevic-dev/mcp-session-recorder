from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.render import (
    render_approvals,
    render_docs,
    render_overview,
    render_replay,
    render_sessions,
)
from app.services.session_service import build_service


class RecollectionRequest(BaseModel):
    prompt: str


app = FastAPI(
    title="MCP Session Recorder",
    version="0.1.0",
    description=(
        "Python FastAPI recorder for MCP session replay, approval history, evidence chains, "
        "and operator-facing audit posture."
    ),
)

SERVICE = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/sessions", response_class=HTMLResponse)
def sessions() -> str:
    return render_sessions()


@app.get("/approvals", response_class=HTMLResponse)
def approvals() -> str:
    return render_approvals()


@app.get("/replay", response_class=HTMLResponse)
def replay() -> str:
    return render_replay()


@app.get("/docs", response_class=HTMLResponse)
def docs() -> str:
    return render_docs()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return SERVICE.summary()


@app.get("/api/sessions")
def sessions_api() -> list[dict]:
    return SERVICE.sessions_board()


@app.get("/api/sessions/{session_id}")
def session_detail(session_id: str) -> dict:
    session = SERVICE.session_detail(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/api/approvals")
def approvals_api() -> list[dict]:
    return SERVICE.approval_board()


@app.get("/api/replay")
def replay_api() -> list[dict]:
    return SERVICE.replay_board()


@app.get("/api/sample")
def sample() -> dict:
    return SERVICE.sample_payload()


@app.post("/api/recollect")
def recollect(request: RecollectionRequest) -> dict:
    return SERVICE.recollection(request.prompt)


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "5018"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
