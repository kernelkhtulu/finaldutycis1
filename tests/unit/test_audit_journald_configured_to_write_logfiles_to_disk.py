#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_journald_configured_to_write_logfiles_to_disk


def mock_audit_journald_configured_to_write_logfiles_to_disk_pass(cmd):
    stdout = [
        'Storage=persistent',
        '',
    ]
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_journald_configured_to_write_logfiles_to_disk_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_journald_configured_to_write_logfiles_to_disk_pass)
def test_audit_journald_configured_to_write_logfiles_to_disk_pass():
    state = audit_journald_configured_to_write_logfiles_to_disk()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_journald_configured_to_write_logfiles_to_disk_fail)
def test_audit_journald_configured_to_write_logfiles_to_disk_fail():
    state = audit_journald_configured_to_write_logfiles_to_disk()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
