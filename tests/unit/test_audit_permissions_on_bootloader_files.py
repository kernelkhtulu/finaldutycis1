#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_permissions_on_bootloader_files


def mock_audit_permissions_on_bootloader_files_pass(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_permissions_on_bootloader_files_fail1(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    if 'efi' in cmd:
        stdout = ['-rwx-r-xr-x. 1 root root 0 Jan 1 0:00 /boot/efi/EFI/pytest']
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_permissions_on_bootloader_files_fail2(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    if 'grub2' in cmd:
        stdout = [
            '-rw-r--r--. 1 root root 0 Jan 1 0:00 /boot/grub2/pytest',
        ]
        returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_permissions_on_bootloader_files_pass)
def test_audit_permissions_on_bootloader_files_pass():
    state = audit_permissions_on_bootloader_files()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_permissions_on_bootloader_files_fail1)
def test_audit_permissions_on_bootloader_files_fail1():
    state = audit_permissions_on_bootloader_files()
    assert state == 1


@patch("cis_audit._shellexec", mock_audit_permissions_on_bootloader_files_fail2)
def test_audit_permissions_on_bootloader_files_fail2():
    state = audit_permissions_on_bootloader_files()
    assert state == 2


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
