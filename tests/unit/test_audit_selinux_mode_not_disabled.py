#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_selinux_mode_not_disabled


def mock_selinux_mode_not_disabled_enforcing(cmd):
    stdout = ['enforcing']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_mode_not_disabled_permissive(cmd):
    stdout = ['permissive']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_mode_not_disabled_disabled(cmd):
    stdout = ['disabled']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_selinux_mode_not_disabled_enforcing)
def test_selinux_not_disabled_enforcing_pass():
    state = audit_selinux_mode_not_disabled()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_mode_not_disabled_permissive)
def test_selinux_not_disabled_permissive_pass():
    state = audit_selinux_mode_not_disabled()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_mode_not_disabled_disabled)
def test_selinux_not_disabled_disabled_fail():
    state = audit_selinux_mode_not_disabled()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
