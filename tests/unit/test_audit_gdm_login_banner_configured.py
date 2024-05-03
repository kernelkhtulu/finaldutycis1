#!/usr/bin/env python3

from unittest.mock import Mock, patch

import pytest

from cis_audit import audit_gdm_login_banner_configured


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=0))
def test_audit_gdm_login_banner_configured_pass(caplog):
    state = audit_gdm_login_banner_configured()
    assert state == 0


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=1))
def test_audit_gdm_login_banner_configured_fail(caplog):
    state = audit_gdm_login_banner_configured()
    assert state == 3


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
def test_audit_gdm_login_banner_configured_skipped(caplog):
    state = audit_gdm_login_banner_configured()
    assert state == -2


if __name__ == "__main__":
    pytest.main([__file__, "--no-cov"])
