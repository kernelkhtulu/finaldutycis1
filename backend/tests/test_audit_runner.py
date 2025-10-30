from backend.app.models.audit import AuditRequest
from backend.app.services.audit_runner import AuditRunner, DEFAULT_QUICK_CHECKS


class DummyEngine:
    def __init__(self, payload):
        self.payload = payload
        self.seen_request = None

    def run(self, request):
        self.seen_request = request
        return self.payload


def make_payload():
    return [
        ("1.1.1.1", "Ensure mounting cramfs filesystems is disabled", 1, "Pass", "12ms"),
        ("1.1.1.2", "Ensure mounting freevxfs filesystems is disabled", 1, "Fail", "11ms"),
        ("1.1.1.3", "Ensure mounting jffs2 filesystems is disabled", 1, "Pass", "9ms"),
        ("1.1", "Filesystem Configuration"),
    ]


def test_quick_mode_injects_default_controls():
    engine = DummyEngine(make_payload())
    runner = AuditRunner(engine=engine)

    request = AuditRequest()
    runner.run(request)

    assert engine.seen_request is not None
    assert engine.seen_request.includes == DEFAULT_QUICK_CHECKS


def test_summary_counts_pass_fail_and_total():
    engine = DummyEngine(make_payload())
    runner = AuditRunner(engine=engine)

    request = AuditRequest(execution_mode="full", includes=["1.1.1.1"])
    run = runner.run(request)

    assert run.summary["Pass"] == 2
    assert run.summary["Fail"] == 1
    assert run.summary["total"] == 3
    assert run.results[0].control_id == "1.1.1.1"
    assert run.results[3].result is None
