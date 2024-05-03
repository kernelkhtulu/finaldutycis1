#!/usr/bin/env python3

from unittest.mock import Mock, patch

import pytest

from cis_audit import audit_gdm_screen_locks


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=0))
def test_audit_gdm_screen_locks_v2_pass(caplog):
    state = audit_gdm_screen_locks()
    assert state == 0


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit.audit_gsettings_option", Mock(return_value=1))
def test_audit_gdm_screen_locks_v2_fail_no_profile(caplog):
    state = audit_gdm_screen_locks()
    assert state == 3


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
def test_audit_gdm_screen_locks_v2_skipped(caplog):
    state = audit_gdm_screen_locks()
    assert state == -2


if __name__ == "__main__":
    pytest.main([__file__, "--no-cov"])
