#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch, Mock

import pytest

from cis_audit import audit_gsettings_option


def mock__shellexec_pass(cmd) -> SimpleNamespace:
    returncode = 0
    stderr = []
    stdout = ["uint32 300"]

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock__shellexec_error(cmd) -> SimpleNamespace:
    returncode = 1
    stderr = ["No such schema ?org.gnome.login-screen?"]
    stdout = []

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


option = "org.gnome.desktop.session idle-delay"


@pytest.mark.parametrize(
    "comparisons",
    [
        pytest.param({'eq': "300"}, id="eq-300"),
        pytest.param({'ne': "0"}, id="ne-0"),
        pytest.param({'ge': 300}, id="ge-300"),
        pytest.param({'ge': 100}, id="ge-100"),
        pytest.param({'gt': 100}, id="gt-100"),
        pytest.param({'le': 300}, id="le-300"),
        pytest.param({'le': 500}, id="le-500"),
        pytest.param({'lt': 500}, id="lt-500"),
    ],
)
@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_pass)
def test_audit_gsettings_option_pass(caplog, comparisons):
    caplog.set_level("INFO")

    state = audit_gsettings_option(option, comparisons)

    assert len(caplog.records) == 0
    assert state == 0


@pytest.mark.parametrize(
    "comparisons,log_message",
    [
        pytest.param({'eq': "0"}, "GSetting %s value %s is not equal to %s", id="eq-0"),
        pytest.param({'ne': "300"}, "GSetting %s value %s is not not-equal to %s", id="ne-300"),
        pytest.param({'ge': 500}, "GSetting %s value %s is not greater than or equal to %s", id="ge-500"),
        pytest.param({'gt': 500}, "GSetting %s value %s is not greater than %s", id="gt-500"),
        pytest.param({'le': 100}, "GSetting %s value %s is not less than or equal to %s", id="le-100"),
        pytest.param({'lt': 100}, "GSetting %s value %s is not less than %s", id="lt-100"),
    ],
)
@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_pass)
def test_audit_gsettings_option_fail(caplog, comparisons, log_message):
    caplog.set_level("INFO")

    state = audit_gsettings_option(option, comparisons)

    assert caplog.records.pop(0).msg == log_message
    assert len(caplog.records) == 0
    assert state == 1


@patch("cis_audit.audit_package_is_installed", Mock(return_value=0))
@patch("cis_audit._shellexec", mock__shellexec_error)
def test_audit_gsettings_option_error(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_option(option, comparisons={'eq': "300"})

    assert len(caplog.records) == 0
    assert state == 1


@patch("cis_audit.audit_package_is_installed", Mock(return_value=1))
@patch("cis_audit._shellexec", mock__shellexec_pass)
def test_audit_gsettings_option_skipped(caplog):
    caplog.set_level("INFO")

    state = audit_gsettings_option(option, comparisons={'eq': "300"})

    assert caplog.records.pop(0).msg == "The glib2 package is required for this test but it is not installed"
    assert len(caplog.records) == 0
    assert state == -2


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
