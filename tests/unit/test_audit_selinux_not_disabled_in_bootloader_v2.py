#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_selinux_not_disabled_in_bootloader_v2


def mock_audit_selinux_not_disabled_in_bootloader_v2_pass(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_selinux_not_disabled_in_bootloader_v2_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 0

    if "grubby" in cmd:
        stdout = ['args="ro spectre_v2=retpoline rhgb quiet selinux=0"']

    elif "GRUB_CMDLINE" in cmd:
        stdout = ['GRUB_CMDLINE_LINUX="spectre_v2=retpoline rhgb quiet enforcing=0"']

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit._shellexec", mock_audit_selinux_not_disabled_in_bootloader_v2_pass)
def test_audit_selinux_not_disabled_in_bootloader_v2_pass():
    state = audit_selinux_not_disabled_in_bootloader_v2()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_selinux_not_disabled_in_bootloader_v2_fail)
def test_audit_selinux_not_disabled_in_bootloader_v2_fail():
    state = audit_selinux_not_disabled_in_bootloader_v2()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__])
