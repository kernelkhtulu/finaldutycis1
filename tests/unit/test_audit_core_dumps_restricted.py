#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_core_dumps_restricted


def mock_core_dumps_pass(cmd):
    if 'limits.conf' in cmd:
        stdout = ['* hard core 0']
        stderr = ['']
        returncode = 0
    elif 'sysctl' in cmd:
        stdout = ['fs.suid_dumpable = 0']
        stderr = ['']
        returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_core_dumps_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_core_dumps_pass)
def test_mock_core_dumps_pass():
    state = audit_core_dumps_restricted()
    assert state == 0


@patch("cis_audit._shellexec", mock_core_dumps_fail)
def test_mock_core_dumps_fail():
    state = audit_core_dumps_restricted()
    assert state == 7


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
