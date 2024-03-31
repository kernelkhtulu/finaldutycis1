#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_etc_shadow_password_fields_are_not_empty


def mock_etc_shadow_password_fields_are_not_empty_pass(cmd):
    returncode = 1
    stderr = ['']
    stdout = ['']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_etc_shadow_password_fields_are_not_empty_fail(cmd):
    returncode = 0
    stderr = ['']
    stdout = ['pytest::18925::::::']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_etc_shadow_password_fields_are_not_empty_pass)
def test_audit_etc_shadow_password_fields_are_not_empty_pass():
    state = audit_etc_shadow_password_fields_are_not_empty()
    assert state == 0


@patch("cis_audit._shellexec", mock_etc_shadow_password_fields_are_not_empty_fail)
def test_audit_etc_shadow_password_fields_are_not_empty_fail():
    state = audit_etc_shadow_password_fields_are_not_empty()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
