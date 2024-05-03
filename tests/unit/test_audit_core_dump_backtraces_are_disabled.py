#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_core_dump_backtraces_are_disabled


def mock_audit_core_dump_backtraces_are_disabled_pass(cmd):
    stdout = ['ProcessSizeMax=0']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_core_dump_backtraces_are_disabled_fail1(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_core_dump_backtraces_are_disabled_fail2(cmd):
    stdout = ['ProcessSizeMax=2G']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit._shellexec", mock_audit_core_dump_backtraces_are_disabled_pass)
def test_audit_core_dump_backtraces_are_disabled_pass():
    state = audit_core_dump_backtraces_are_disabled()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_core_dump_backtraces_are_disabled_fail1)
def test_audit_core_dump_backtraces_are_disabled_fail1():
    state = audit_core_dump_backtraces_are_disabled()
    assert state == 1


@patch("cis_audit._shellexec", mock_audit_core_dump_backtraces_are_disabled_fail2)
def test_audit_core_dump_backtraces_are_disabled_fail2():
    state = audit_core_dump_backtraces_are_disabled()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__])
