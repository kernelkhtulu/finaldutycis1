#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_service_is_enabled_and_is_active


def mock_disabled_and_inactive(cmd, **kwargs):
    if 'is-active' in cmd:
        output = ['inactive']
    elif 'is-enabled' in cmd:
        output = ['disabled']

    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_enabled_and_active(cmd, **kwargs):
    if 'is-active' in cmd:
        output = ['active']
    elif 'is-enabled' in cmd:
        output = ['enabled']

    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_enabled_and_active)
def test_service_is_enabled_and_is_active_pass():
    state = audit_service_is_enabled_and_is_active("pytest")
    assert state == 0


@patch("cis_audit._shellexec", mock_disabled_and_inactive)
def test_service_is_enabled_and_is_active_fail():
    state = audit_service_is_enabled_and_is_active("pytest")
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
