import datetime

from django import template

from apps.warranty import models

register = template.Library()

@register.filter(name='warranty_current_status')
def get_current_status(rekla_id):
	"""
	Custom Django Templatetag to return the current status of a 
		warranty ticket
	"""

	return models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].get_status_display()

@register.filter(name='warranty_last_update')
def get_last_update(rekla_id):
	"""
	Custom Django Templatetag to display the number of days since last
		status update of a warranty ticket
	"""

	last_update = models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days

@register.filter(name='warranty_last_update_date')
def get_last_update_date(rekla_id):
	"""
	Custom Django Templatetag to display the date of the last update of a warranty ticket
	"""

	last_update_date = models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].date

	return last_update_date