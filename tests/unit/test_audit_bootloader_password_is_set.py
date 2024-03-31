#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_bootloader_password_is_set


def mock_bootloader_password_pass(cmd):
    output = ['GRUB2_PASSWORD=supersecret']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_bootloader_password_fail_blank(cmd):
    output = ['']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_bootloader_password_fail_commented(cmd):
    output = ['#GRUB2_PASSWORD=supersecret']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_bootloader_password_error(cmd):
    raise Exception


@patch("cis_audit._shellexec", mock_bootloader_password_pass)
def test_bootloader_password_set_pass():
    state = audit_bootloader_password_is_set()
    assert state == 0


@patch("cis_audit._shellexec", mock_bootloader_password_fail_blank)
def test_bootloader_password_set_fail_blank():
    state = audit_bootloader_password_is_set()
    assert state == 1


@patch("cis_audit._shellexec", mock_bootloader_password_fail_commented)
def test_bootloader_password_set_fail_commented():
    state = audit_bootloader_password_is_set()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
