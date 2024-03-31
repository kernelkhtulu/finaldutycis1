#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_iptables_is_flushed


def mock_iptables_is_flushed_pass(cmd, **kwargs):
    output = ['']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_iptables_is_flushed_fail(cmd, **kwargs):
    output = [
        '-A INPUT -i lo -j ACCEPT',
    ]
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_iptables_is_flushed_pass)
def test_iptables_is_flushed_pass():
    state = audit_iptables_is_flushed()
    assert state == 0


@patch("cis_audit._shellexec", mock_iptables_is_flushed_fail)
def test_iptables_is_flushed_fail():
    state = audit_iptables_is_flushed()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
