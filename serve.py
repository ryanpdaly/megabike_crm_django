# -*- coding: utf-8 -*-

import os
import django
import webbrowser
from threading import Timer

os.environ["DJANGO_SETTINGS_MODULE"] = "megabike_crm.settings"
django.setup()

import cherrypy
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

class DjangoApplication(object):
	HOST = "192.168.0.152"
	PORT = 8080

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

		cherrypy.engine.block()

	def exit(self):
		cherrypy.engine.exit()

if __name__ == "__main__":
	print("Your app is running at http://192.168.0.152:8080")
	DjangoApplication().run()