"""FastAPI entrypoint for the NovaShield backend."""

from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .. import __version__ as package_version  # type: ignore
from .core.config import Settings, get_settings
from .models.audit import AuditRequest, AuditRun
from .services.audit_runner import AuditRunner

settings = get_settings()
runner = AuditRunner(history_size=settings.history_size)

app = FastAPI(
    title=settings.app_name,
    version=package_version,
    description=(
        "NovaShield transforms the legacy cis_audit engine into a responsive, "
        "insight-heavy compliance platform."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_runner() -> AuditRunner:
    """FastAPI dependency that returns the shared audit runner."""

    return runner


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict:
    """Simple readiness endpoint for load balancers and monitoring."""

    return {"status": "ok", "app": settings.app_name, "version": package_version}


@app.get("/api/audits", response_model=List[AuditRun])
async def list_audits(
    limit: int = Query(default=5, ge=1, le=settings.history_size),
    audit_runner: AuditRunner = Depends(get_runner),
) -> List[AuditRun]:
    """Return the most recent audit runs."""

    return audit_runner.list_runs(limit=limit)


@app.post("/api/audits/run", response_model=AuditRun)
async def run_audit(
    payload: AuditRequest,
    audit_runner: AuditRunner = Depends(get_runner),
) -> AuditRun:
    """Execute an audit synchronously and return the fresh result."""

    return audit_runner.run(payload)
