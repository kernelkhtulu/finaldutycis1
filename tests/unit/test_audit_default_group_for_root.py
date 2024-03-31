#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_default_group_for_root


def mock_default_group_for_root_pass(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['0']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_default_group_for_root_fail(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['1']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_default_group_for_root_pass)
def test_audit_default_group_for_root_pass():
    state = audit_default_group_for_root()
    assert state == 0


@patch("cis_audit._shellexec", mock_default_group_for_root_fail)
def test_audit_default_group_for_root_fail():
    state = audit_default_group_for_root()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
