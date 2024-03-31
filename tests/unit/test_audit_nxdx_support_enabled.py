#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_nxdx_support_enabled


def mock_nxdx_support_pass(cmd):
    stdout = ['[    0.000000] NX (Execute Disable) protection: active']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nxdx_support_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_nxdx_support_pass)
def test_nxdx_support_enabled_pass():
    state = audit_nxdx_support_enabled()
    assert state == 0


@patch("cis_audit._shellexec", mock_nxdx_support_fail)
def test_nxdx_support_enabled_fail():
    state = audit_nxdx_support_enabled()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
