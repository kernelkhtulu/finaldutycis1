#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_nftables_base_chains_exist


def mock_nftables_base_chains_exist_pass(cmd):
    returncode = 0
    stderr = ['']

    if 'input' in cmd:
        stdout = ['type filter hook input priority 0;']
    elif 'forward' in cmd:
        stdout = ['type filter hook forward priority 0;']
    elif 'output' in cmd:
        stdout = ['type filter hook output priority 0;']
    else:
        stdout = ['']
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nftables_base_chains_exist_fail_input(cmd):
    returncode = 0
    stderr = ['']

    if 'input' in cmd:
        stdout = ['']
        returncode = 1
    elif 'forward' in cmd:
        stdout = ['type filter hook forward priority 0;']
    elif 'output' in cmd:
        stdout = ['type filter hook output priority 0;']
    else:
        stdout = ['']
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nftables_base_chains_exist_fail_forward(cmd):
    returncode = 0
    stderr = ['']

    if 'input' in cmd:
        stdout = ['type filter hook input priority 0;']
    elif 'forward' in cmd:
        stdout = ['']
        returncode = 1
    elif 'output' in cmd:
        stdout = ['type filter hook output priority 0;']
    else:
        stdout = ['']
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nftables_base_chains_exist_fail_output(cmd):
    returncode = 0
    stderr = ['']

    if 'input' in cmd:
        stdout = ['type filter hook input priority 0;']
    elif 'forward' in cmd:
        stdout = ['type filter hook forward priority 0;']
    elif 'output' in cmd:
        stdout = ['']
        returncode = 1
    else:
        stdout = ['']
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nftables_base_chains_exist_fail_all(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_nftables_base_chains_exist_pass)
def test_audit_nftables_base_chains_exist_pass():
    state = audit_nftables_base_chains_exist()
    assert state == 0


@patch("cis_audit._shellexec", mock_nftables_base_chains_exist_fail_input)
def test_audit_nftables_base_chains_exist_fail_input():
    state = audit_nftables_base_chains_exist()
    assert state == 1


@patch("cis_audit._shellexec", mock_nftables_base_chains_exist_fail_forward)
def test_audit_nftables_base_chains_exist_fail_forward():
    state = audit_nftables_base_chains_exist()
    assert state == 2


@patch("cis_audit._shellexec", mock_nftables_base_chains_exist_fail_output)
def test_audit_nftables_base_chains_exist_fail_output():
    state = audit_nftables_base_chains_exist()
    assert state == 4


@patch("cis_audit._shellexec", mock_nftables_base_chains_exist_fail_all)
def test_audit_nftables_base_chains_exist_fail_all():
    state = audit_nftables_base_chains_exist()
    assert state == 7


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
