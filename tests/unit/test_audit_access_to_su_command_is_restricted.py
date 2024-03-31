#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_access_to_su_command_is_restricted


def mock_access_to_su_command_is_restricted_pass(cmd):
    returncode = 0
    stderr = ['']

    if '/etc/pam.d/su' in cmd:
        stdout = ['auth required pam_wheel.so use_uid group=<group_name>']
    elif '/etc/group' in cmd:
        stdout = ['pytest:x:1000:']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_access_to_su_command_not_restricted_fail(cmd):
    returncode = 0
    stderr = ['']

    if '/etc/pam.d/su' in cmd:
        stdout = ['']
    elif '/etc/group' in cmd:
        stdout = ['pytest:x:1000:pyuser']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_access_to_su_command_is_restricted_fail_with_users_in_group(cmd):
    returncode = 0
    stderr = ['']

    if '/etc/pam.d/su' in cmd:
        stdout = ['auth required pam_wheel.so use_uid group=<group_name>']
    elif '/etc/group' in cmd:
        stdout = ['pytest:x:1000:pyuser']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_access_to_su_command_is_restricted_pass)
def test_audit_access_to_su_command_is_restricted_pass():
    state = audit_access_to_su_command_is_restricted()
    assert state == 0


@patch("cis_audit._shellexec", mock_access_to_su_command_not_restricted_fail)
def test_audit_access_to_su_command_is_restricted_fail():
    state = audit_access_to_su_command_is_restricted()
    assert state == 1


@patch("cis_audit._shellexec", mock_access_to_su_command_is_restricted_fail_with_users_in_group)
def test_audit_access_to_su_command_is_restricted_fail_with_users_in_group():
    state = audit_access_to_su_command_is_restricted()
    assert state == 2


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
