import functools
import logging
import math
import os
import pwd

from crontab import CronTab
from tornado.ioloop import PeriodicCallback


log_crontab = logging.getLogger("tornado-crontab.crontab")
FORMAT_LOG_CRONTAB = " ".join(["tornado-crontab[%(pid)d]:",
                               "(%(user)s)",
                               "FUNC",
                               "(%(funcname)s",
                               "%(args)s %(kwargs)s)"])


class CronTabCallback(PeriodicCallback):

    def __init__(self, callback, schedule, io_loop=None):
        self.__crontab = CronTab(schedule)
        super(CronTabCallback, self).__init__(
            callback, self._calc_callbacktime(), io_loop)
        self.pid = os.getpid()
        self.user = (os.environ.get("USERNAME")
                     if os.name == "nt" else pwd.getpwuid(os.getuid()).pw_name)

    def _calc_callbacktime(self, now=None):
        return math.ceil(self.__crontab.next(now)) * 1000.0

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


def crontab(schedule, io_loop=None):

    def receive_func(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            _func = functools.partial(func, *args, **kwargs)
            CronTabCallback(_func, schedule, io_loop).start()

        return wrapper
    return receive_func
