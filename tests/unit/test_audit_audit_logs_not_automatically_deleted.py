#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_audit_logs_not_automatically_deleted


def mock_audit_logs_not_automatically_deleted_pass(cmd):
    stdout = ['max_log_file = keep_logs', '']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_logs_not_automatically_deleted_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_logs_not_automatically_deleted_pass)
def test_audit_audit_logs_not_automatically_deleted_pass():
    state = audit_audit_logs_not_automatically_deleted()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_logs_not_automatically_deleted_fail)
def test_audit_audit_logs_not_automatically_deleted_fail():
    state = audit_audit_logs_not_automatically_deleted()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
