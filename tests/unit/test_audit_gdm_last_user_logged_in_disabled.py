#!/usr/bin/env python3

from unittest.mock import mock_open, patch, Mock

import pytest

from cis_audit import audit_gdm_last_user_logged_in_disabled


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
def test_audit_gdm_last_user_logged_in_disabled_error_not_installed():
    state = audit_gdm_last_user_logged_in_disabled()
    assert state == -2


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
def test_audit_gdm_last_user_logged_in_disabled_fail_files_not_found():
    state = audit_gdm_last_user_logged_in_disabled()
    assert state == 17


@patch("builtins.open", mock_open())
@patch("os.path.exists", return_value=True)
@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
def test_audit_gdm_last_user_logged_in_disabled_fail(MagickMock):
    state = audit_gdm_last_user_logged_in_disabled()
    assert state == 46


@patch("builtins.open", mock_open(read_data='user-db:user\nsystem-db:gdm\nfile-db:/usr/share/gdm/greeter-dconf-defaults\n[org/gnome/login-screen]\ndisable-user-list=true'))
@patch("os.path.exists", return_value=True)
@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
def test_audit_gdm_last_user_logged_in_disabled_pass(MagickMock):
    state = audit_gdm_last_user_logged_in_disabled()
    assert state == 0


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
