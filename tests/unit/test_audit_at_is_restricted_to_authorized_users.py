#!/usr/bin/env python3

import os
from unittest.mock import patch

import pytest

from cis_audit import audit_at_is_restricted_to_authorized_users


@patch.object(os.path, "exists", return_value=False)
@patch("cis_audit.audit_file_permissions", return_value=0)
def test_audit_at_is_restricted_to_authorized_users_pass(*args):
    state = audit_at_is_restricted_to_authorized_users()
    assert state == 0


@patch.object(os.path, "exists", return_value=True)
@patch("cis_audit.audit_file_permissions", return_value=1)
def test_audit_at_is_restricted_to_authorized_users_fail(*args):
    state = audit_at_is_restricted_to_authorized_users()
    assert state == 3


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
