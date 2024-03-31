#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_mta_is_localhost_only


def mock_mta_pass(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_mta_fail(cmd):
    stdout = ['0.0.0.0:25']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_mta_pass)
def test_mta_is_localhost_pass():
    state = audit_mta_is_localhost_only()
    assert state == 0


@patch("cis_audit._shellexec", mock_mta_fail)
def test_mta_is_localhost_fail():
    state = audit_mta_is_localhost_only()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
