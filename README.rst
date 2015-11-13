Tornado Crontab
===============

Tornado Crontab is a library that can make the task apps like Crontab.

Hello, CronTab
--------------

Here is an example every minute task app.::

	import tornado.ioloop
	import tornado_crontab
	
	def hello_crontab():
	
		print("Hello, CronTab")
	
	if __name__ == "__main__":
	
		tornado_crontab.CronTabCallback(hello_crontab, "* * * * *").start()
		tornado.ioloop.IOLoop.instance().start()	
