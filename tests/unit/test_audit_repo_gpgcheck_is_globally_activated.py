#!/usr/bin/env python3

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from cis_audit import audit_repo_gpgcheck_is_globally_activated


def mock_repo_gpgcheck_activated_pass(cmd):
    stdout = ['repo_gpgcheck=1']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def mock_repo_gpgcheck_activated_fail(cmd):
    stdout = ['repo_gpgcheck=0']
    stderr = ['']
    returncode = 0

    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


@patch("cis_audit._shellexec", mock_repo_gpgcheck_activated_pass)
def test_audit_repo_gpgcheck_is_globally_activated_pass():
    state = audit_repo_gpgcheck_is_globally_activated()
    assert state == 0


@patch("cis_audit._shellexec", mock_repo_gpgcheck_activated_fail)
def test_audit_repo_gpgcheck_is_globally_activated_fail():
    state = audit_repo_gpgcheck_is_globally_activated()
    assert state == 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
