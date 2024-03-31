#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_duplicate_group_names


def mock_duplicate_group_names_pass(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_duplicate_group_names_fail(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['pytest']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_duplicate_group_names_pass)
def test_audit_duplicate_group_names_pass():
    state = audit_duplicate_group_names()
    assert state == 0


@patch("cis_audit._shellexec", mock_duplicate_group_names_fail)
def test_audit_duplicate_group_names_fail():
    state = audit_duplicate_group_names()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
