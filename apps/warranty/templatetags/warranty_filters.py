import datetime

from django import template

from apps.warranty import models

register = template.Library()

@register.filter(name='warranty_current_status')
def get_current_status(rekla_id):
	return models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].get_status_display()

@register.filter(name='warranty_last_update')
def get_last_update(rekla_id):
	last_update = models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days

@register.filter(name='warranty_last_update_date')
def get_last_update_date(rekla_id):
	last_update_date = models.ReklaStatusUpdate.objects.filter(rekla_ticket=rekla_id).order_by('-id')[0].date

	return last_update_date