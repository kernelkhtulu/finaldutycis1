#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_service_is_masked


def mock_masked(*args, **kwargs):
    output = ['masked']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_unmasked(*args, **kwargs):
    output = ['enabled']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_error(*args, **kwargs):
    output = ['']
    error = ['Failed to get unit file state for pytest.service: No such file or directory']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_masked)
def test_service_masked_pass():
    state = audit_service_is_masked(service="pytest")
    assert state == 0


@patch("cis_audit._shellexec", mock_unmasked)
def test_service_masked_fail():
    state = audit_service_is_masked(service="pytest")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
