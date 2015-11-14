===============
tornado-crontab
===============

tornado-crontab is a library that can make the task apps like crontab.

|travis|

Usage
=====

Here is an example every minute task app::

    import tornado.ioloop
    import tornado_crontab
    
    def hello_crontab():
    
        print("Hello, CronTab")
    
    if __name__ == "__main__":
    
        tornado_crontab.CronTabCallback(hello_crontab, "* * * * *").start()
        tornado.ioloop.IOLoop.instance().start()    

Using
=====

* `Tornado <http://www.tornadoweb.org/>`_
* `crontab <https://github.com/josiahcarlson/parse-crontab/>`_

License
=======

* tornado-crontab license under the `MIT license <https://github.com/gaujin/tornado-crontab/blob/master/LICENSE>`_.
* `Tornado is licensed under the Apache license <https://github.com/tornadoweb/tornado/blob/master/LICENSE>`_.
* `crontab is licensed under the LGPL license version 2.1 <https://github.com/josiahcarlson/parse-crontab/blob/master/LICENSE>`_.

See the LICENSE file for specific terms.

.. |travis| image:: https://travis-ci.org/gaujin/tornado-crontab.svg?branch=master
    :target: https://travis-ci.org/gaujin/tornado-crontab