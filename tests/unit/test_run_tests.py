#!/usr/bin/env python3

import argparse
from datetime import datetime
from unittest.mock import patch

import pytest

from cis_audit import run_tests


def default():
    pass


def mock_run_tests_pass(*args, **kwargs):
    return 0


def mock_run_tests_fail(*args, **kwargs):
    return 1


def mock_run_tests_error(*args, **kwargs):
    return -1


def mock_run_tests_skipped(*args, **kwargs):
    return -2


def mock_run_tests_kwargs(*args, **kwargs):
    return 0


def mock_run_tests_exception(*args, **kwargs):
    raise Exception


def mock_datetime_utcnow(offset=0):
    return datetime(year=1, month=1, day=1)


@patch("cis_audit.CONFIG", argparse.Namespace(includes=None, excludes=None, level=0, log_level="DEBUG", system_type="server"))
@patch("cis_audit._get_utcnow", mock_datetime_utcnow)
class TestRunTests:

    test_args = {
        'type': "test",
        'levels': {'server': 1, 'workstation': 1},
        'description': "pytest",
    }
    test_id = "1.1"

    def test_run_tests_pass(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_pass
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Pass',
                'duration': '0ms',
            }
        ]

    def test_run_tests_fail(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_fail
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Fail',
                'duration': '0ms',
            }
        ]

    def test_run_tests_error(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_error
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Error',
                'duration': '0ms',
            }
        ]

    def test_run_tests_exception(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_exception
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Error',
                'duration': '0ms',
            }
        ]

    def test_run_tests_skipped(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_skipped
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Skipped',
                'duration': '0ms',
            }
        ]

    def test_run_tests_kwargs(self):
        test_args = self.test_args.copy()
        test_args['function'] = mock_run_tests_kwargs
        test_args['kwargs'] = {'foo': 'bar'}
        test_args.pop('levels')
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': None,
                'result': 'Pass',
                'duration': '0ms',
            }
        ]

    def test_run_tests_type_header(self):
        test_args = self.test_args.copy()
        test_args['type'] = 'header'
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
            }
        ]

    def test_run_tests_type_manual(self):
        test_args = self.test_args.copy()
        test_args['type'] = 'manual'
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Manual',
            }
        ]

    def test_run_tests_type_none(self, caplog):
        test_args = self.test_args.copy()
        test_args.pop('type', None)
        tests_dict = {self.test_id: test_args}

        caplog.set_level("DEBUG")

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Not Implemented',
            }
        ]
        assert caplog.records[0].msg == "Test 1.1 does not explicitly define a type, so assuming it is a test"
        assert caplog.records[1].msg == "Checking whether to run test 1.1"
        assert caplog.records[2].msg == "Including test 1.1"

    def test_run_tests_type_skip(self, caplog):
        test_args = self.test_args.copy()
        test_args['type'] = 'skip'
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Skipped',
            }
        ]

    def test_run_tests_error_not_implemented(self, caplog):
        test_args = self.test_args.copy()
        test_args.pop('type')
        tests_dict = {self.test_id: test_args}

        result = run_tests(tests_dict)
        assert result == [
            {
                '_id': self.test_id,
                'description': test_args['description'],
                'level': test_args['levels']['server'],
                'result': 'Not Implemented',
            }
        ]


if __name__ == '__main__':
    pytest.main([__file__, '--no-cov'])
