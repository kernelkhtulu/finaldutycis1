#!/usr/bin/env python3

import pytest

from cis_audit import _shellexec


def test_shellexec_stdout_pass():
    result = _shellexec('echo stdout')
    assert result.returncode == 0
    assert result.stdout == ['stdout']
    assert result.stderr == ['']


def test_shellexec_sterr_pass():
    result = _shellexec('echo stderr | tee /dev/stderr 1>/dev/null')
    assert result.returncode == 0
    assert result.stdout == ['']
    assert result.stderr == ['stderr']


def test_shellexec_sterr_error():
    result = _shellexec('error pytest')
    assert result.returncode == 127
    assert result.stderr == ['/bin/sh: error: command not found']
    assert result.stdout == ['']


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
