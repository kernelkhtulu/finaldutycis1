#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_partition_is_separate


def mock_parition_exists(cmd):
    output = ['/dev/sda1            1014M  125M  890M  13% /boot']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_parititon_not_exists(cmd):
    output = ['']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_parition_exists)
def test_partition_is_separate():
    state = audit_partition_is_separate(partition="/dev/sda1")
    assert state == 0


@patch("cis_audit._shellexec", mock_parititon_not_exists)
def test_partition_is_not_separate():
    state = audit_partition_is_separate(partition="/dev/sda1")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
