#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_nftables_table_exists


def mock_nftables_table_exists_pass(cmd):
    stdout = ['table inet filter']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_nftables_table_exists_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_nftables_table_exists_pass)
def test_audit_nftables_table_exists_pass():
    state = audit_nftables_table_exists()
    assert state == 0


@patch("cis_audit._shellexec", mock_nftables_table_exists_fail)
def test_audit_nftables_table_exists_fail():
    state = audit_nftables_table_exists()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
