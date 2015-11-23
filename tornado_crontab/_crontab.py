import functools
import math

from crontab import CronTab
from tornado.ioloop import PeriodicCallback


class CronTabCallback(PeriodicCallback):

    def __init__(self, callback, schedule, io_loop=None):
        self.__crontab = CronTab(schedule)
        super(CronTabCallback, self).__init__(
                callback, self._calc_callbacktime(), io_loop)

    def _calc_callbacktime(self, now=None):
        return math.ceil(self.__crontab.next(now)) * 1000.0

    def _run(self):

        if self._running:
            # TODO: here write of run log
            pass

        return PeriodicCallback._run(self)

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
