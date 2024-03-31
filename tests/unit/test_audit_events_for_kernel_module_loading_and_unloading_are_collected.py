#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_events_for_kernel_module_loading_and_unloading_are_collected


def mock_audit_events_for_kernel_module_loading_and_unloading_are_collected_pass(cmd):
    if 'auditctl' in cmd:
        stdout = [
            '-w /sbin/insmod -p x -k modules',
            '-w /sbin/rmmod -p x -k modules',
            '-w /sbin/modprobe -p x -k modules',
            '-a always,exit -F arch=b64 -S init_module,delete_module -F key=modules',
        ]
    else:
        stdout = [
            '-w /sbin/insmod -p x -k modules',
            '-w /sbin/rmmod -p x -k modules',
            '-w /sbin/modprobe -p x -k modules',
            '-a always,exit -F arch=b64 -S init_module -S delete_module -k modules',
        ]
    stderr = ['']
    returncode = 0

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


def mock_audit_events_for_kernel_module_loading_and_unloading_are_collected_fail(cmd):
    stdout = ['']
    stderr = ['']
    returncode = 1

    return SimpleNamespace(returncode=returncode, stderr=stderr, stdout=stdout)


@patch("cis_audit._shellexec", mock_audit_events_for_kernel_module_loading_and_unloading_are_collected_pass)
def test_audit_events_for_kernel_module_loading_and_unloading_are_collected_pass():
    state = audit_events_for_kernel_module_loading_and_unloading_are_collected()
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_events_for_kernel_module_loading_and_unloading_are_collected_fail)
def test_audit_events_for_kernel_module_loading_and_unloading_are_collected_fail():
    state = audit_events_for_kernel_module_loading_and_unloading_are_collected()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
