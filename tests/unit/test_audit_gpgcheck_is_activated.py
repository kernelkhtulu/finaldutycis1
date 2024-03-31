#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_gpgcheck_is_activated


def mock_gpgcheck_activated_pass(cmd):
    if 'yum.conf' in cmd:
        output = ['gpgcheck=1']
        error = ['']
        returncode = 0

    elif 'yum.repos.d' in cmd:
        output = ['']
        error = ['']
        returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_gpgcheck_activated_fail_state_1(cmd):
    if 'yum.conf' in cmd:
        output = ['gpgcheck=0']
        error = ['']
        returncode = 0

    elif 'yum.repos.d' in cmd:
        output = ['']
        error = ['']
        returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_gpgcheck_activated_fail_state_2(cmd):
    if 'yum.conf' in cmd:
        output = ['gpgcheck=1']
        error = ['']
        returncode = 0

    elif 'yum.repos.d' in cmd:
        output = ['base does not have gpgcheck enabled']
        error = ['']
        returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_gpgcheck_activated_fail_state_3(cmd):
    if 'yum.conf' in cmd:
        output = ['gpgcheck=0']
        error = ['']
        returncode = 0

    elif 'yum.repos.d' in cmd:
        output = ['base does not have gpgcheck enabled.']
        error = ['']
        returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_gpgcheck_activated_pass)
def test_check_gpgcheck_is_activated_pass():
    state = audit_gpgcheck_is_activated()
    assert state == 0


@patch("cis_audit._shellexec", mock_gpgcheck_activated_fail_state_1)
def test_check_gpgcheck_is_activated_fail_state_1():
    state = audit_gpgcheck_is_activated()
    assert state == 1


@patch("cis_audit._shellexec", mock_gpgcheck_activated_fail_state_2)
def test_check_gpgcheck_is_activated_fail_state_2():
    state = audit_gpgcheck_is_activated()
    assert state == 2


@patch("cis_audit._shellexec", mock_gpgcheck_activated_fail_state_3)
def test_check_gpgcheck_is_activated_fail_state_3():
    state = audit_gpgcheck_is_activated()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
