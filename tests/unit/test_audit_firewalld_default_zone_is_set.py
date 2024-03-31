#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_firewalld_default_zone_is_set


def mock_firewalld_default_zone_is_set(*args):
    output = ['public', '']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_firewalld_not_running(cmd):
    output = ['']
    error = ['FirewallD is not running']
    returncode = 252

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_firewalld_default_zone_is_set)
def test_firewalld_defaullt_zone_set_pass():
    state = audit_firewalld_default_zone_is_set()
    assert state == 0


@patch("cis_audit._shellexec", mock_firewalld_not_running)
def test_firewalld_not_running():
    state = audit_firewalld_default_zone_is_set()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
