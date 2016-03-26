===============
tornado-crontab
===============

tornado-crontab is a library that can make the task apps like crontab.

|travis| |requires|

Installation
============

Automatic installation::

   $ pip install tornado-crontab

torando-crontab is listed in `PyPI <https://pypi.python.org/pypi/tornado-crontab>`_ and can be installed with pip or easy_install.

Manual installation::

   $ git clone https://github.com/gaujin/tornado-crontab.git
   $ cd tornado-crontab
   $ python setup.py install

tornado-crontab source code is `hosted on GitHub <https://github.com/gaujin/tornado-crontab>`_

Usage
=====

Here is an example every minute task app::

   from __future__ import print_function
   import functools
   import tornado.ioloop
   import tornado_crontab
    
   def hello_crontab(value):
    
       print("Hello, {0}".format(value))
    
   if __name__ == "__main__":
    
       _func = functools.partial(hello_crontab, *["crontab"])
       tornado_crontab.CronTabCallback(_func, "* * * * *").start()
       tornado.ioloop.IOLoop.instance().start()    

decorator style task app::

   from __future__ import print_function
   import tornado.ioloop
   from tornado_crontab import crontab
    
   @crontab("* * * * *")
   def hello_crontab(value):

       print("Hello, {0}".format(value))

   if __name__ == "__main__":

       hello_crontab("crontab")
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

.. |requires| image:: https://requires.io/github/gaujin/tornado-crontab/requirements.svg?branch=master
     :target: https://requires.io/github/gaujin/tornado-crontab/requirements/?branch=master
     :alt: Requirements Status
