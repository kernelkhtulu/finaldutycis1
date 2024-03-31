#!/usr/bin/env python3

from unittest.mock import patch

import pytest

from cis_audit import audit_package_not_installed_or_service_is_masked


def mock_result_pass(*args, **kwargs):
    return 0


def mock_result_fail(*args, **kwargs):
    return 1


@patch("cis_audit.audit_package_is_installed", mock_result_fail)
@patch("cis_audit.audit_service_is_masked", mock_result_fail)
def test_audit_package_not_installed_or_service_is_masked_pass_not_installed():
    state = audit_package_not_installed_or_service_is_masked(package='pytest', service='pytestd')
    assert state == 0


@patch("cis_audit.audit_package_is_installed", mock_result_pass)
@patch("cis_audit.audit_service_is_masked", mock_result_pass)
def test_audit_package_not_installed_or_service_is_masked_pass_masked():
    state = audit_package_not_installed_or_service_is_masked(package='pytest', service='pytestd')
    assert state == 0


@patch("cis_audit.audit_package_is_installed", mock_result_pass)
@patch("cis_audit.audit_service_is_masked", mock_result_fail)
def test_audit_package_not_installed_or_service_is_masked_fail():
    state = audit_package_not_installed_or_service_is_masked(package='pytest', service='pytestd')
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
