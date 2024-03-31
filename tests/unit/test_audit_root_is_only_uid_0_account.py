#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_root_is_only_uid_0_account


def mock_root_is_only_uid_0_account_pass(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['root']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_root_is_only_uid_0_account_fail(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['root', 'pytest']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_root_is_only_uid_0_account_pass)
def test_audit_root_is_only_uid_0_account_pass():
    state = audit_root_is_only_uid_0_account()
    assert state == 0


@patch("cis_audit._shellexec", mock_root_is_only_uid_0_account_fail)
def test_audit_root_is_only_uid_0_account_fail():
    state = audit_root_is_only_uid_0_account()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
