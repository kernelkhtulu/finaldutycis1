#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_removable_partition_option_is_set


def mock_option_set(cmd):
    if 'lsblk' in cmd:
        output = ['/mnt']
    else:
        output = ['']

    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_option_not_set(cmd):
    if 'lsblk' in cmd:
        output = ['/mnt']
    else:
        output = ['/mnt   /dev/sdb1 vfat ro,relatime']

    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_option_set)
def test_partition_option_is_set():
    state = audit_removable_partition_option_is_set(option="noexec")
    assert state == 0


@patch("cis_audit._shellexec", mock_option_not_set)
def test_partition_option_is_not_set():
    state = audit_removable_partition_option_is_set(option="noexec")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
