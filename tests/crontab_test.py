from __future__ import print_function

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from datetime import datetime
import functools
import logging
import os
import time
import unittest

from freezegun import freeze_time


class FakeTimeIOLoop(object):

    def __init__(self, freezer):
        self._offset = 0
        self._freezer = freezer

    def time(self):
        return time.time() + self._offset

    def add_timeout(self, timeout, callback):
        self._callback = (timeout, callback)

    def call_later(self, timeout, callback):
        self._max = timeout

    def close(self):
        pass

    def start(self):
        for _ in range(self._max):
            _timeout, _callback = self._callback
            self._freezer.stop()
            self._freezer.time_to_freeze = datetime.utcfromtimestamp(_timeout)
            self._freezer.start()
            _callback()
            self._offset = _timeout - time.time()

    def stop(self):
        pass


class TestCronTabCallback(unittest.TestCase):

    BEGIN_TIME = "2015-11-08T00:00:00Z"

    def __init__(self, *args, **kwargs):
        super(TestCronTabCallback, self).__init__(*args, **kwargs)

    def setUp(self):
        unittest.TestCase.setUp(self)

        self._freezer = freeze_time(self.BEGIN_TIME)
        self._freezer.start()
        self.io_loop = FakeTimeIOLoop(self._freezer)
        self.calls = []

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self._freezer.stop()

    def crontab_task(self):
        self.calls.append(datetime.utcfromtimestamp(
            self.io_loop.time()).strftime("%Y-%m-%dT%H:%M:%S"))

    def _target(self, schedule):

        from tornado_crontab import CronTabCallback

        pc = CronTabCallback(self.crontab_task, schedule, self.io_loop)
        pc.start()

    def _test(self, schedule, asserts):

        self._target(schedule)
        self.io_loop.call_later(10, self.io_loop.stop)
        self.io_loop.start()

        self.assertEqual(self.calls, asserts)

    def test_every_minute(self):

        self._test("* * * * *", ["2015-11-08T00:01:00", "2015-11-08T00:02:00",
                                 "2015-11-08T00:03:00", "2015-11-08T00:04:00",
                                 "2015-11-08T00:05:00", "2015-11-08T00:06:00",
                                 "2015-11-08T00:07:00", "2015-11-08T00:08:00",
                                 "2015-11-08T00:09:00", "2015-11-08T00:10:00"])

    def test_every_hour(self):

        self._test("0 * * * *", ["2015-11-08T01:00:00", "2015-11-08T02:00:00",
                                 "2015-11-08T03:00:00", "2015-11-08T04:00:00",
                                 "2015-11-08T05:00:00", "2015-11-08T06:00:00",
                                 "2015-11-08T07:00:00", "2015-11-08T08:00:00",
                                 "2015-11-08T09:00:00", "2015-11-08T10:00:00"])

    def test_every_day(self):

        self._test("0 0 * * *", ["2015-11-09T00:00:00", "2015-11-10T00:00:00",
                                 "2015-11-11T00:00:00", "2015-11-12T00:00:00",
                                 "2015-11-13T00:00:00", "2015-11-14T00:00:00",
                                 "2015-11-15T00:00:00", "2015-11-16T00:00:00",
                                 "2015-11-17T00:00:00", "2015-11-18T00:00:00"])

    def test_every_monday(self):

        self._test("0 0 * * 1", ["2015-11-09T00:00:00", "2015-11-16T00:00:00",
                                 "2015-11-23T00:00:00", "2015-11-30T00:00:00",
                                 "2015-12-07T00:00:00", "2015-12-14T00:00:00",
                                 "2015-12-21T00:00:00", "2015-12-28T00:00:00",
                                 "2016-01-04T00:00:00", "2016-01-11T00:00:00"])

    def test_every_month(self):

        self._test("0 0 1 * *", ["2015-12-01T00:00:00", "2016-01-01T00:00:00",
                                 "2016-02-01T00:00:00", "2016-03-01T00:00:00",
                                 "2016-04-01T00:00:00", "2016-05-01T00:00:00",
                                 "2016-06-01T00:00:00", "2016-07-01T00:00:00",
                                 "2016-08-01T00:00:00", "2016-09-01T00:00:00"])

    def test_every_year(self):

        self._test("0 0 1 1 *", ["2016-01-01T00:00:00", "2017-01-01T00:00:00",
                                 "2018-01-01T00:00:00", "2019-01-01T00:00:00",
                                 "2020-01-01T00:00:00", "2021-01-01T00:00:00",
                                 "2022-01-01T00:00:00", "2023-01-01T00:00:00",
                                 "2024-01-01T00:00:00", "2025-01-01T00:00:00"])


class TestCrontabDecorator(TestCronTabCallback):

    def __init__(self, *args, **kwargs):
        super(TestCrontabDecorator, self).__init__(*args, **kwargs)

    def _target(self, schedule):

        from tornado_crontab import crontab

        @crontab(schedule, self.io_loop)
        def decorate_task():
            self.crontab_task()

        decorate_task()


class TestCrontabLogging(unittest.TestCase):

    def test__get_func_spec_no_args(self):

        from tornado_crontab import CronTabCallback

        def _func():
            pass

        _crontab = CronTabCallback(_func, "* * * * *")
        self.assertEqual((_func, [], {}), _crontab._get_func_spec())

    def test__get_func_spec_args(self):

        from tornado_crontab import CronTabCallback

        def _func(arg1, arg2):
            pass

        _args = ["value1", "value2"]
        _crontab = CronTabCallback(
            functools.partial(_func, *_args), "* * * * *")
        self.assertEqual((_func, _args, {}), _crontab._get_func_spec())

        _crontab = CronTabCallback(
            functools.partial(
                functools.partial(_func, _args[0]), _args[1]), "* * * * *")
        self.assertEqual((_func, _args, {}), _crontab._get_func_spec())

    def test__get_func_spec_kwargs(self):

        from tornado_crontab import CronTabCallback

        def _func(arg1, arg2):
            pass

        _kwargs = {"arg1": "value1", "arg2": "value2"}
        _crontab = CronTabCallback(
            functools.partial(_func, **_kwargs), "* * * * *")
        self.assertEqual((_func, [], _kwargs), _crontab._get_func_spec())

        _crontab = CronTabCallback(
            functools.partial(
                functools.partial(_func, arg1="value1"), arg2="value2"),
            "* * * * *")
        self.assertEqual((_func, [], _kwargs), _crontab._get_func_spec())

    def test__logging(self):

        from tornado_crontab import CronTabCallback
        from tornado_crontab._crontab import log_crontab

        def _func(arg1, arg2):
            pass

        _crontab = CronTabCallback(
            functools.partial(_func, "value1", arg2="value2"), "* * * * *")
        _crontab._running = True

        _stream = StringIO()
        log_crontab.addHandler(logging.StreamHandler(_stream))
        _crontab._logging(logging.DEBUG)
        _log = _stream.getvalue()

        # for windows
        if os.name == "nt":
            user = os.environ.get("USERNAME")

        # for other os
        else:
            import pwd
            user = pwd.getpwuid(os.geteuid()).pw_name

        self.assertEqual(
            " ".join(["tornado-crontab[%d]:" % os.getpid(), "(%s)" % user,
                      "FUNC (_func ['value1'] {'arg2': 'value2'})\n"]), _log)


if __name__ == "__main__":
    unittest.main()
