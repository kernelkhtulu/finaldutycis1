#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_shadow_group_is_empty


def mock_shadow_group_is_empty(cmd):
    output = ['']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_shadow_group_is_not_empty(cmd):
    output = ['user']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_shadow_group_is_absent(cmd):
    output = ['']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_shadow_group_is_empty)
def test_audit_shadow_group_is_empty_pass():
    state = audit_shadow_group_is_empty()
    assert state == 0


@patch("cis_audit._shellexec", mock_shadow_group_is_absent)
def test_audit_shadow_group_is_absent_pass():
    state = audit_shadow_group_is_empty()
    assert state == 0


@patch("cis_audit._shellexec", mock_shadow_group_is_not_empty)
def test_audit_shadow_group_is_empty_fail():
    state = audit_shadow_group_is_empty()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
