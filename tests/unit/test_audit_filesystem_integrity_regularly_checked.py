#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_filesystem_integrity_regularly_checked


def mock_filesystem_integrity_pass_cron(cmd):
    output = ['/etc/cron.d/aide-check']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_filesystem_integrity_pass_systemd(cmd, *args, **kwargs):
    if 'is-enabled' in cmd:
        output = ['enabled']
        error = ['']
        returncode = 0
    elif 'is-active' in cmd:
        output = ['active']
        error = ['']
        returncode = 0
    else:
        output = ['']
        error = ['']
        returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_filesystem_integrity_fail(cmd):
    output = ['']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_filesystem_integrity_error(cmd):
    raise Exception


@patch("cis_audit._shellexec", mock_filesystem_integrity_pass_cron)
def test_filesystem_integrity_pass_crond():
    state = audit_filesystem_integrity_regularly_checked()
    assert state == 0


@patch("cis_audit._shellexec", mock_filesystem_integrity_pass_systemd)
def test_filesystem_integrity_pass_systemd():
    state = audit_filesystem_integrity_regularly_checked()
    assert state == 0


@patch("cis_audit._shellexec", mock_filesystem_integrity_fail)
def test_filesystem_integrity_fail():
    state = audit_filesystem_integrity_regularly_checked()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
