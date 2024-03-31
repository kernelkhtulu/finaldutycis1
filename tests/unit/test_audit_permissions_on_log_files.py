#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_permissions_on_log_files


def mock_audit_permissions_on_log_files_are_configured_pass(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_permissions_on_log_files_are_configured_fail(cmd):
    stdout = [
        '-rw-r--r--. 1 root root 0 Jan 1 0:00 /var/log/pytest',
        '',
    ]
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_permissions_on_log_files_are_configured_pass)
def test_audit_permissions_on_log_files_are_configured_pass():
    state = audit_permissions_on_log_files()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_permissions_on_log_files_are_configured_fail)
def test_audit_permissions_on_log_files_are_configured_fail():
    state = audit_permissions_on_log_files()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
