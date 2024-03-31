#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_password_expiration_warning_is_configured


def mock_password_expiration_warning_is_configured_pass(cmd):
    returncode = 0
    stderr = ['']

    if 'PASS_WARN_AGE' in cmd:
        stdout = ['PASS_WARN_AGE    7']
    elif 'shadow' in cmd:
        stdout = [
            'root:7',
            'vagrant:7',
        ]

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_password_expiration_warning_is_configured_fail(cmd):
    returncode = 0
    stderr = ['']

    if 'PASS_WARN_AGE' in cmd:
        stdout = ['PASS_WARN_AGE    0']
    elif 'shadow' in cmd:
        stdout = [
            'root:0',
            'vagrant:0',
        ]

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_password_expiration_warning_is_configured_pass)
def test_audit_password_expiration_warning_is_configured_pass():
    state = audit_password_expiration_warning_is_configured()
    assert state == 0


@patch("cis_audit._shellexec", mock_password_expiration_warning_is_configured_fail)
def test_audit_password_expiration_warning_is_configured_pass_fail():
    state = audit_password_expiration_warning_is_configured()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
