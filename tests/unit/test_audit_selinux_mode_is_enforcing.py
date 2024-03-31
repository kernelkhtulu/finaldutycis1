#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_selinux_mode_is_enforcing


def mock_selinux_mode_is_enforcing_enforcing(cmd):
    stdout = ['enforcing']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_mode_is_enforcing_permissive(cmd):
    stdout = ['permissive']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_selinux_mode_is_enforcing_disabled(cmd):
    stdout = ['disabled']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_selinux_mode_is_enforcing_enforcing)
def test_selinux_is_enforcing_enforcing_pass():
    state = audit_selinux_mode_is_enforcing()
    assert state == 0


@patch("cis_audit._shellexec", mock_selinux_mode_is_enforcing_permissive)
def test_selinux_is_enforcing_permissive_pass():
    state = audit_selinux_mode_is_enforcing()
    assert state == 3


@patch("cis_audit._shellexec", mock_selinux_mode_is_enforcing_disabled)
def test_selinux_is_enforcing_disabled_fail():
    state = audit_selinux_mode_is_enforcing()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
