import functools
import inspect
import logging
import math
import os
import warnings

from crontab import CronTab
from tornado.ioloop import PeriodicCallback


log_crontab = logging.getLogger("tornado-crontab.crontab")
FORMAT_LOG_CRONTAB = " ".join(["tornado-crontab[%(pid)d]:",
                               "(%(user)s)",
                               "FUNC",
                               "(%(funcname)s",
                               "%(args)s %(kwargs)s)"])

IS_TZ_SUPPORTED = "default_utc" in inspect.getargspec(CronTab.next).args
UNSUPPORTED_MESSAGE = """\
Since crontab package version is low, UTC can not be used.
When using it with UTC, upgrade the crontab package to 0.22.0+."""


class CronTabCallback(PeriodicCallback):
    """ Crontab Callback Class

    Schedule execution of the function.
    Timezone is local time by default.
    If you want to schedule with UTC, set `is_utc` to `True`.
    """

    def __init__(self, callback, schedule, is_utc=False):
        """ CrontabCallback initializer

        .. note::
            If Timezone is not supported and `is_utc` is set to `True`,
            a warning is output and `is_utc` is ignored.

        :type callback: func
        :param callback: target schedule function
        :type schedule: str
        :param schedule: crotab expression
        :type is_utc: bool
        :param is_utc: schedule timezone is UTC. (True:UTC, False:Local Timezone)
        """

        # If Timezone is not supported and `is_utc` is set to `True`,
        # a warning is output and `is_utc` is ignored.
        if not IS_TZ_SUPPORTED and is_utc:
            warnings.warn(UNSUPPORTED_MESSAGE)
            is_utc = False

        self.__crontab = CronTab(schedule)
        self.__is_utc = is_utc

        super(CronTabCallback, self).__init__(
            callback, self._calc_callbacktime())

        self.pid = os.getpid()

        if os.name == "nt":
            self.user = os.environ.get("USERNAME")
        else:
            import pwd
            self.user = pwd.getpwuid(os.geteuid()).pw_name

    def _calc_callbacktime(self, now=None):

        _kwargs = dict(now=now)

        if IS_TZ_SUPPORTED:
            _kwargs.update(dict(default_utc=self.__is_utc))

        return math.ceil(
            self.__crontab.next(**_kwargs)) * 1000.0

    def _get_func_spec(self):

        _args = []
        _kwargs = {}

        def _get_func(_func):

            if not isinstance(_func, functools.partial):
                return _func

            for _arg in reversed(_func.args):
                _args.insert(0, _arg)

            if _func.keywords:
                _kwargs.update(_func.keywords)

            return _get_func(_func.func)

        _func = _get_func(self.callback)
        return _func, _args, _kwargs

    def _logging(self, level):

        if self._running and log_crontab.isEnabledFor(level):

            _func, _args, _kwargs = self._get_func_spec()

            log_crontab.log(level,
                            FORMAT_LOG_CRONTAB % dict(pid=self.pid,
                                                      user=self.user,
                                                      funcname=_func.__name__,
                                                      args=_args,
                                                      kwargs=_kwargs))

    def _run(self):

        self._logging(logging.INFO)

        try:
            PeriodicCallback._run(self)

        finally:

            self._logging(logging.DEBUG)

    def _schedule_next(self):
        self.callback_time = self._calc_callbacktime()
        super(CronTabCallback, self)._schedule_next()


def crontab(schedule, is_utc=False):
    """ Crontab Decorator

    Decorate this function to the function you want to execute as scheduled.
    Timezone is local time by default.
    If you want to schedule with UTC, set `is_utc` to `True`.

    .. note::
        If Timezone is not supported and `is_utc` is set to `True`,
        a warning is output and `is_utc` is ignored.

    :type schedule: str
    :param schedule: crotab expression
    :type is_utc: bool
    :param is_utc: schedule timezone is UTC. (True:UTC, False:Local Timezone)
    :rtype: func
    :return: scheduled execute function
    """

    def receive_func(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            _func = functools.partial(func, *args, **kwargs)
            CronTabCallback(_func, schedule=schedule,
                            is_utc=is_utc).start()

        return wrapper
    return receive_func
