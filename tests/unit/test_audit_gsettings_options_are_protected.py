#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch, Mock

import pytest

from cis_audit import audit_gsettings_options_are_protected

options = (
    "org.gnome.desktop.session.idle-delay",
    "org.gnome.desktop.screensaver.lock-delay",
)

def mock__shellexec_pass(cmd) -> SimpleNamespace:
    returncode = 0
    stderr = [""]
    stdout = ["true"]

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock__shellexec_fail(cmd) -> SimpleNamespace:
    returncode = 0
    stderr = [""]
    stdout = ["false"]

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock__shellexec_error(cmd) -> SimpleNamespace:
    returncode = 1
    stderr = [""]
    stdout = [""]

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_pass)
def test_audit_gsettings_option_is_protected_pass(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_options_are_protected(options)
    assert len(caplog.records) == 0
    assert state == 0


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_fail)
def test_audit_gsettings_option_is_protected_fail(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_options_are_protected(options)
    assert caplog.records.pop(0).msg == "The gsetting option '%s' is not protected"
    assert caplog.records.pop(0).msg == "The gsetting option '%s' is not protected"
    assert len(caplog.records) == 0
    assert state == 3


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_error)
def test_audit_gsettings_option_is_protected_error(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_options_are_protected(options)
    assert caplog.records.pop(0).msg == "Failed to check gsetting option '%s'"
    assert len(caplog.records) == 0
    assert state == -1


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
@patch("cis_audit._shellexec", mock__shellexec_pass)
def test_audit_gsettings_option_is_protected_skipped(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_options_are_protected(options)

    assert caplog.records.pop(0).msg == "The glib2 package is required for this test but it is not installed"
    assert len(caplog.records) == 0
    assert state == -2


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
