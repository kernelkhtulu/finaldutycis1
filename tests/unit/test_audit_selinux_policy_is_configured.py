#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_selinux_policy_is_configured


def mock_selinux_policy_configured_pass_mls(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    if 'SELINUXTYPE' in cmd:
        stdout = ["SELINUXTYPE=mls"]

    elif 'sestatus' in cmd:
        stdout = ['Loaded policy name:             mls']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_policy_configured_pass_targeted(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    if 'SELINUXTYPE' in cmd:
        stdout = ["SELINUXTYPE=targeted"]

    elif 'sestatus' in cmd:
        stdout = ['Loaded policy name:             targeted']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_policy_configured_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_selinux_policy_configured_pass_mls)
def test_selinux_policy_configured_pass_mls():
    state = audit_selinux_policy_is_configured()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_policy_configured_pass_targeted)
def test_selinux_policy_configured_pass_targeted():
    state = audit_selinux_policy_is_configured()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_policy_configured_fail)
def test_selinux_policy_configured_fail():
    state = audit_selinux_policy_is_configured()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
