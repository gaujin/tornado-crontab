import math

from crontab import CronTab
from tornado.ioloop import PeriodicCallback


class CronTabCallback(PeriodicCallback):

    def __init__(self, callback, crontab, io_loop=None):
        self.__crontab = CronTab(crontab)
        super(CronTabCallback, self).__init__(
                callback, self._calc_callbacktime(), io_loop)

    def _calc_callbacktime(self, now=None):
        return math.ceil(self.__crontab.next(now)) * 1000.0

    def _schedule_next(self):
        self.callback_time = self._calc_callbacktime()
        super(CronTabCallback, self)._schedule_next()
