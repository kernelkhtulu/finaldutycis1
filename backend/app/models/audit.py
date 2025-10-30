"""Pydantic models that describe audit requests and responses for NovaShield."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class BenchmarkSelector(BaseModel):
    """Identify which CIS benchmark catalog should back an audit run."""

    platform: str = Field(
        default="centos7",
        description="Identifier for the benchmark platform (e.g. centos7, rhel8).",
    )
    version: str = Field(
        default="3.1.2",
        description="CIS benchmark version to execute for the selected platform.",
    )


class AuditRequest(BaseModel):
    """Incoming API payload instructing the engine how to execute an audit."""

    benchmark: BenchmarkSelector = Field(default_factory=BenchmarkSelector)
    includes: List[str] = Field(
        default_factory=list,
        description="Optional list of specific control identifiers to include.",
    )
    excludes: List[str] = Field(
        default_factory=list,
        description="Optional list of specific control identifiers to exclude.",
    )
    level: int = Field(
        default=0,
        ge=0,
        le=2,
        description="When non-zero, limit execution to the specified CIS level.",
    )
    system_type: Literal["server", "workstation"] = Field(
        default="server",
        description="Select the column of the benchmark to evaluate levels from.",
    )
    execution_mode: Literal["quick", "full"] = Field(
        default="quick",
        description="Quick mode runs a curated subset of controls for rapid feedback.",
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="WARNING",
        description="Control the verbosity of the underlying audit engine logs.",
    )


class AuditResult(BaseModel):
    """Normalized representation of a single benchmark control outcome."""

    control_id: str
    description: str
    level: Optional[int] = None
    result: Optional[str] = None
    duration: Optional[str] = None


class AuditRun(BaseModel):
    """Full response returned to clients once an audit completes."""

    run_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: Literal["running", "completed", "failed"]
    benchmark: BenchmarkSelector
    level: int
    system_type: str
    execution_mode: str
    summary: Dict[str, int] = Field(default_factory=dict)
    results: List[AuditResult] = Field(default_factory=list)
    error_message: Optional[str] = None

    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()},
    }
