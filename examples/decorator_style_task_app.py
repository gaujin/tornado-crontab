from __future__ import print_function
import tornado.ioloop
from tornado_crontab import crontab


@crontab("* * * * *")
def hello_crontab(value):

    print("Hello, {0}".format(value))


if __name__ == "__main__":

    hello_crontab("crontab")
    tornado.ioloop.IOLoop.instance().start()
