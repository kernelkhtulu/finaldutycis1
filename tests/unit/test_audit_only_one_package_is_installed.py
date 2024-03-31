#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_only_one_package_is_installed


def mock_packages_one_installed(*args):
    output = ['chrony-0.0.0']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_packages_not_installed(cmd):
    output = ['']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_packages_both_installed(cmd):
    output = [
        'chrony-0.0.0',
        'ntp-0.0.0',
    ]
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_package_error(cmd):
    output = ['']
    error = ['rpm: no arguments given for query']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


packages = 'chrony ntp'


@patch("cis_audit._shellexec", mock_packages_one_installed)
def test_audit_only_one_package_is_installed_pass():
    state = audit_only_one_package_is_installed(packages=packages)
    assert state == 0


@patch("cis_audit._shellexec", mock_packages_both_installed)
def test_audit_only_one_package_is_installed_fail_both_installed():
    state = audit_only_one_package_is_installed(packages=packages)
    assert state == 1


@patch("cis_audit._shellexec", mock_packages_not_installed)
def test_audit_only_one_package_is_installed_fail_neither_installed():
    state = audit_only_one_package_is_installed(packages=packages)
    assert state == 1


@patch("cis_audit._shellexec", mock_package_error)
def test_audit_only_one_package_is_installed_error():
    state = audit_only_one_package_is_installed(packages=packages)
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
