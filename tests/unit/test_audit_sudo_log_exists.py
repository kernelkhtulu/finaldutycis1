#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_sudo_log_exists


def mock_sudo_log_exists_pass(*args, **kwargs):
    output = ['Defaults logfile="/var/log/sudo.log"']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_sudo_log_exists_fail(*args, **kwargs):
    output = ['']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_sudo_log_exists_pass)
def test_sudo_log_exists_pass():
    state = audit_sudo_log_exists()
    assert state == 0


@patch("cis_audit._shellexec", mock_sudo_log_exists_fail)
def test_sudo_log_exists_fail():
    state = audit_sudo_log_exists()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
