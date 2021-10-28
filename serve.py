# -*- coding: utf-8 -*-

import os
import django
import logging
import webbrowser

from threading import Timer

os.environ["DJANGO_SETTINGS_MODULE"] = "megabike_crm.settings"
django.setup()

import cherrypy
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from apps.scheduled_tasks.management import startup_scheduler

class DjangoApplication(object):
	HOST = settings.HOST
	PORT = settings.PORT

	scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
	scheduler.add_jobstore(DjangoJobStore(), 'default')

	def mount_static(self, url, root):
		"""
		:param url: Relative url
		:param root: Path to static files root
		"""
		config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': root,
			'tools.expires.on': True,
			'tools.expires.secs': 86400

		}
		cherrypy.tree.mount(None, url, {'/': config})

	def open_browser(self):
		Timer(3, webbrowser.open, (f'http://{self.HOST}:{self.PORT}',)).start()

	def run(self):
		cherrypy.config.update({
			'server.socket_host': self.HOST,
			'server.socket_port': self.PORT,
			'engine.autoreload_on': False,
			'log.screen': True,

			'server.ssl_module': 'builtin',
			'server.ssl_certificate': 'ssl_certs/cert.pem',
			'server.ssl_private_key': 'ssl_certs/privkey.pem',
		})
		self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)

		cherrypy.log("Loading and serving Django application")
		cherrypy.tree.graft(WSGIHandler())
		cherrypy.engine.start()

		# self.open_browser()

		if settings.SCHEDULER_AUTOSTART is True:
			DjangoApplication().start_apscheduler()
			scheduler.log("Scheduler initiated")

		cherrypy.engine.block()

	def exit(self):
		cherrypy.engine.exit()

	def start_apscheduler(self):
		if settings.DEBUG:
			logging.getLogger('apscheduler').setLevel(logging.INFO)
		else:
			logging.getLogger('apscheduler').setLevel(logging.WARNING)

		self.scheduler.add_job(
			startup_scheduler.email_faellig_versicherung,
			trigger=CronTrigger(minute="*/1"),
			id="insurance_email",
			max_instances=1,
			replace_existing=True
		)

		scheduler.start()

if __name__ == "__main__":
	print(f"Your app is running at https://{DjangoApplication.HOST}:{DjangoApplication.PORT}")
	DjangoApplication().run()

	'''
	if settings.SCHEDULER_AUTOSTART is True:
		DjangoApplication().start_apscheduler()
		scheduler.log("Scheduler initiated")
	'''