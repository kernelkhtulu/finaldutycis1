"""Service orchestration for executing audits and tracking history."""

from __future__ import annotations

import uuid
from collections import Counter, deque
from datetime import datetime, timezone
from threading import Lock
from typing import Deque, Iterable, List, Optional

from ..models.audit import AuditRequest, AuditResult, AuditRun
from .cis_engine import CisBenchmarkEngine

DEFAULT_QUICK_CHECKS = [
    "1.1.1.1",
    "1.1.1.2",
    "1.1.1.3",
    "1.1.2",
    "1.1.5",
    "1.3.1",
    "2.2.1",
    "3.1.1",
    "4.1.1.1",
    "5.3.1",
    "6.2.1",
]


class AuditRunner:
    """Execute audits via a pluggable engine and retain a rolling history."""

    def __init__(
        self,
        engine: Optional[CisBenchmarkEngine] = None,
        history_size: int = 10,
    ) -> None:
        self._engine = engine or CisBenchmarkEngine()
        self._history: Deque[AuditRun] = deque(maxlen=history_size)
        self._lock = Lock()

    def list_runs(self, limit: Optional[int] = None) -> List[AuditRun]:
        """Return the most recent audit runs, newest first."""

        with self._lock:
            snapshot = list(self._history)

        if limit is not None:
            return snapshot[: limit]
        return snapshot

    def run(self, request: AuditRequest) -> AuditRun:
        """Execute an audit synchronously and persist the result in history."""

        run_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc)
        run = AuditRun(
            run_id=run_id,
            started_at=started_at,
            status="running",
            benchmark=request.benchmark,
            level=request.level,
            system_type=request.system_type,
            execution_mode=request.execution_mode,
        )

        try:
            prepared = self._prepare_request(request)
            raw_results = self._engine.run(prepared)
            results = self._transform_results(raw_results)
            run.results = results
            run.summary = self._summarise(results)
            run.status = "completed"
        except Exception as exc:  # pragma: no cover - surface to client
            run.status = "failed"
            run.error_message = str(exc)
        finally:
            run.completed_at = datetime.now(timezone.utc)
            with self._lock:
                self._history.appendleft(run)

        return run

    def _prepare_request(self, request: AuditRequest) -> AuditRequest:
        """Apply NovaShield defaults (e.g. quick run subsets) when needed."""

        if request.execution_mode == "quick" and not request.includes:
            return request.model_copy(update={"includes": DEFAULT_QUICK_CHECKS})
        return request

    @staticmethod
    def _transform_results(raw_results: Iterable[tuple]) -> List[AuditResult]:
        """Convert the legacy tuple structure into typed audit results."""

        results: List[AuditResult] = []

        for record in raw_results:
            control_id = record[0]
            description = record[1] if len(record) >= 2 else ""
            level = record[2] if len(record) >= 3 else None
            result = record[3] if len(record) >= 4 else None
            duration = record[4] if len(record) >= 5 else None

            results.append(
                AuditResult(
                    control_id=control_id,
                    description=description,
                    level=level,
                    result=result,
                    duration=duration,
                )
            )

        return results

    @staticmethod
    def _summarise(results: Iterable[AuditResult]) -> dict[str, int]:
        """Count pass/fail/error totals for quick dashboards."""

        bucket = Counter()

        for entry in results:
            if entry.result:
                bucket[entry.result] += 1

        if bucket:
            bucket["total"] = sum(bucket.values())

        return dict(bucket)
