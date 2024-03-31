#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_package_not_installed


def mock_package_installed(*args):
    output = ['pytest-0.0.0', '']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_package_not_installed(cmd):
    output = ['package pytest is not installed', '']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_package_not_installed)
def test_package_not_installed_pass():
    state = audit_package_not_installed("pytest")
    assert state == 0


@patch("cis_audit._shellexec", mock_package_installed)
def test_package_not_installed_fail():
    state = audit_package_not_installed("pytest")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
