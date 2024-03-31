#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_journald_configured_to_compress_large_logs


def mock_audit_journald_configured_to_compress_large_logs_pass(cmd):
    stdout = [
        'Compress=yes',
        '',
    ]
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_journald_configured_to_compress_large_logs_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_journald_configured_to_compress_large_logs_pass)
def test_audit_journald_configured_to_compress_large_logs_pass():
    state = audit_journald_configured_to_compress_large_logs()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_journald_configured_to_compress_large_logs_fail)
def test_audit_journald_configured_to_compress_large_logs_fail():
    state = audit_journald_configured_to_compress_large_logs()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
