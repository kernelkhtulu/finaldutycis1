#!/usr/bin/env python3

from unittest.mock import Mock, patch

import pytest

from cis_audit import audit_gdm_automount_is_disabled


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=0))
def test_audit_gdm_automount_is_disabled_pass(caplog):
    state = audit_gdm_automount_is_disabled()
    assert state == 0


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=1))
def test_audit_gdm_automount_is_disabled_fail(caplog):
    state = audit_gdm_automount_is_disabled()
    assert state == 3


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
def test_audit_gdm_automount_is_disabled_skipped(caplog):
    state = audit_gdm_automount_is_disabled()
    assert state == -2


if __name__ == "__main__":
    pytest.main([__file__, "--no-cov"])
