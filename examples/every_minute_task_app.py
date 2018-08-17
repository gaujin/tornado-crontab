from __future__ import print_function
import functools
import tornado.ioloop
import tornado_crontab


def hello_crontab(value):

    print("Hello, {0}".format(value))


if __name__ == "__main__":

    _func = functools.partial(hello_crontab, *["crontab"])
    tornado_crontab.CronTabCallback(_func, "* * * * *").start()
    tornado.ioloop.IOLoop.current().start()
