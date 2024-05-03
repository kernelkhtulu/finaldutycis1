#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_yum_updates


def mock_audit_yum_updates_pass(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_yum_updates_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 100

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_yum_updates_stderr(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit._shellexec", mock_audit_yum_updates_pass)
def test_audit_yum_updates_pass():
    state = audit_yum_updates()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_yum_updates_fail)
def test_audit_yum_updates_fail():
    state = audit_yum_updates()
    assert state == 2


@patch("cis_audit._shellexec", mock_audit_yum_updates_stderr)
def test_audit_yum_updates_stderr():
    state = audit_yum_updates()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__])
