#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_selinux_policy_is_configured


def mock_selinux_policy_configured_pass(cmd):
    stdout = ['targeted']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_policy_configured_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_selinux_policy_configured_pass)
def test_selinux_policy_configured_pass():
    state = audit_selinux_policy_is_configured()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_policy_configured_fail)
def test_selinux_policy_configured_fail():
    state = audit_selinux_policy_is_configured()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
