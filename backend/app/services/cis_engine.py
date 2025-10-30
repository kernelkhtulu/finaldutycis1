"""Wrapper that adapts the legacy audit engine for NovaShield's service layer."""

from __future__ import annotations

from types import SimpleNamespace
from typing import List, Tuple

from cis_audit import CISAudit, benchmarks

from ..models.audit import AuditRequest


class CisBenchmarkEngine:
    """Execute benchmark runs using the bundled cis_audit module."""

    def run(self, request: AuditRequest) -> List[Tuple]:
        platform = request.benchmark.platform
        version = request.benchmark.version

        try:
            test_matrix = benchmarks[platform][version]
        except KeyError as exc:  # pragma: no cover - defensive guard
            raise ValueError(
                f"Unknown benchmark combination '{platform}:{version}'."
            ) from exc

        config = SimpleNamespace(
            includes=request.includes or None,
            excludes=request.excludes or None,
            level=request.level,
            system_type=request.system_type,
            log_level=request.log_level,
        )

        audit = CISAudit(config=config)
        return audit.run_tests(test_matrix)
