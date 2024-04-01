#!/usr/bin/env python3

from unittest.mock import mock_open, patch

import pytest

from cis_audit import audit_gdm_login_banner_configured


def mock_audit_package_is_installed_true(*args, **kwargs):
    return 0


def mock_audit_package_is_installed_false(*args, **kwargs):
    return 1


@patch("cis_audit.audit_package_is_installed", mock_audit_package_is_installed_false)
def test_audit_gdm_login_banner_configured_skipped():
    state = audit_gdm_login_banner_configured()
    assert state == -2


@patch("cis_audit.audit_package_is_installed", mock_audit_package_is_installed_true)
def test_audit_gdm_login_banner_configured_fail_files_not_found():
    state = audit_gdm_login_banner_configured()
    assert state == 17


@patch("builtins.open", mock_open())
@patch("os.path.exists", return_value=True)
@patch("cis_audit.audit_package_is_installed", mock_audit_package_is_installed_true)
def test_audit_gdm_login_banner_configured_fail(MagickMock):
    state = audit_gdm_login_banner_configured()
    assert state == 46


@patch("builtins.open", mock_open(read_data='user-db:user\nsystem-db:gdm\nfile-db:/usr/share/gdm/greeter-dconf-defaults\n[org/gnome/login-screen]\nbanner-message-enable=true\nbanner-message-text='))
@patch("os.path.exists", return_value=True)
@patch("cis_audit.audit_package_is_installed", mock_audit_package_is_installed_true)
def test_audit_gdm_login_banner_configured_pass(MagickMock):
    state = audit_gdm_login_banner_configured()
    assert state == 0


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
