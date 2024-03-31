#!/usr/bin/env python3

from datetime import datetime

import pytest

from cis_audit import _get_utcnow


def test_get_utcnow():
    testtime = _get_utcnow()
    realtime = datetime.utcnow()
    timediff = realtime - testtime

    assert timediff.seconds < 1


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
