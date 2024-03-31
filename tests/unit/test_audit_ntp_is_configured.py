#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_ntp_is_configured


def mock_ntp_configured_pass(cmd):
    if 'is-enabled' in cmd:
        stdout = ['enabled']
    elif 'is-active' in cmd:
        stdout = ['active']
    elif 'server' in cmd:
        stdout = ['server 0.centos.pool.ntp.org iburst', 'server 1.centos.pool.ntp.org iburst', 'server 2.centos.pool.ntp.org iburst', 'server 3.centos.pool.ntp.org iburst']
    elif 'restrict' in cmd:
        stdout = ['restrict -4 default kod nomodify notrap nopeer noquery', 'restrict -6 default kod nomodify notrap nopeer noquery']
    elif 'ps aux' in cmd:
        stdout = ['/usr/sbin/ntpd -u ntp:ntp -g']

    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_ntp_configured_fail(cmd):
    if 'is-enabled' in cmd:
        stdout = ['disabled']
        returncode = 0
    elif 'is-active' in cmd:
        stdout = ['inactive']
        returncode = 0
    elif 'server' in cmd:
        stdout = ['']
        returncode = 1
    elif 'restrict' in cmd:
        stdout = ['']
        returncode = 1
    elif 'ps aux' in cmd:
        stdout = ['']
        returncode = 1

    stderr = ['']

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_ntp_configured_pass)
def test_ntp_is_configured_pass():
    state = audit_ntp_is_configured()
    assert state == 0


@patch("cis_audit._shellexec", mock_ntp_configured_fail)
def test_ntp_is_configured_fail():
    state = audit_ntp_is_configured()
    assert state == 31


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
