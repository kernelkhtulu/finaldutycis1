#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_login_banner_content_is_appropriate


def mock_audit_login_banner_content_is_appropriate_pass(cmd):
    stdout = [""]
    stderr = [""]
    returncode = 1

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_audit_login_banner_content_is_appropriate_fail(cmd):
    stdout = [
        R"\s \r \v",
        "Welcome to CentOS Linux",
    ]
    stderr = [""]
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit._shellexec", mock_audit_login_banner_content_is_appropriate_pass)
def test_audit_login_banner_content_is_appropriate_pass():
    state = audit_login_banner_content_is_appropriate(file="/etc/motd")
    assert state == 0


@patch("cis_audit._shellexec", mock_audit_login_banner_content_is_appropriate_fail)
def test_audit_login_banner_content_is_appropriate_fail():
    state = audit_login_banner_content_is_appropriate(file="/etc/motd")
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__])
