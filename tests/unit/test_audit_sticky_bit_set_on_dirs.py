#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_sticky_bit_on_world_writable_dirs


def mock_sticky_bit_set(cmd):
    output = ['']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_sticky_bit_not_set(cmd):
    output = ['/pytest']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_sticky_bit_error(cmd):
    output = ['']
    error = ['find: invalid expression; I was expecting to find a \')\' somewhere but did not see one.']
    returncode = 123

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


@patch("cis_audit._shellexec", mock_sticky_bit_set)
def test_directory_sticky_bit_is_set():
    state = audit_sticky_bit_on_world_writable_dirs()
    assert state == 0


@patch("cis_audit._shellexec", mock_sticky_bit_not_set)
def test_directory_sticky_bit_is_not_set():
    state = audit_sticky_bit_on_world_writable_dirs()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
