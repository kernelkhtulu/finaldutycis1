#!/usr/bin/env python3

from datetime import datetime

import pytest

from cis_audit import result_stats


@pytest.mark.parametrize(
    "end_time_str,expected_duration",
    [
        pytest.param("1970-01-01T00:01:00+0000", "60", id="slow"),
        pytest.param("1970-01-01T00:00:05+0000", "5.0", id="fast"),
    ],
)
def test_result_stats(end_time_str, expected_duration):
    results = [
        {'result': "Error"},
        {'result': "Fail"},
        {'result': "Fail"},
        {'result': "Not Implemented"},
        {'result': "Pass"},
        {'result': "Pass"},
        {'result': "Pass"},
        {'result': "Skipped"},
    ]
    datefmt = "%Y-%m-%dT%H:%M:%S%z"
    start_time = datetime.strptime("1970-01-01T00:00:00+0000", datefmt)
    end_time = datetime.strptime(end_time_str, datefmt)

    stats = result_stats(results=results, start_time=start_time, end_time=end_time)

    assert str(stats['duration']) == expected_duration
    assert stats['errors'] == 1
    assert stats['failed'] == 2
    assert stats['passed'] == 3
    assert stats['skipped'] == 1

    # assert stats is None


if __name__ == "__main__":
    pytest.main([__file__, "--no-cov"])
