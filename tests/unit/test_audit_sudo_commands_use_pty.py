#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_sudo_commands_use_pty


def mock_sudo_use_pty_pass(*args, **kwargs):
    output = ['Defaults use_pty']
    error = ['']
    returncode = 0

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_sudo_use_pty_fail(*args, **kwargs):
    output = ['']
    error = ['']
    returncode = 1

    return SimpleNamespace(stdout=output, stderr=error, returncode=returncode)


def mock_sudo_use_pty_error(*args, **kwargs):
    raise Exception


@patch("cis_audit._shellexec", mock_sudo_use_pty_pass)
def test_sudo_use_pty_pass():
    state = audit_sudo_commands_use_pty()
    assert state == 0


@patch("cis_audit._shellexec", mock_sudo_use_pty_fail)
def test_sudo_use_pty_fail():
    state = audit_sudo_commands_use_pty()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
