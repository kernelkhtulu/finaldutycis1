#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_service_is_enabled


def mock_disabled(*args, **kwargs):
    output = ['disabled']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_enabled(*args, **kwargs):
    output = ['enabled']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_enabled)
def test_service_enabled_pass():
    state = audit_service_is_enabled("pytest")
    assert state == 0


@patch("cis_audit._shellexec", mock_disabled)
def test_service_enabled_fail():
    state = audit_service_is_enabled("pytest")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
