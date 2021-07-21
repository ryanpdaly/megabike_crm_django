import datetime

from django import template

from apps.insurance import models

register = template.Library()

@register.filter(name='insurance_current_status')
def get_current_status(schaden):
	return models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].get_status_display()

# TODO: Rename to days_since_last_update or something in that direction
@register.filter(name='insurance_last_update')
def get_last_update(schaden):
	last_update = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days

@register.filter(name='insurance_last_update_date')
def get_last_update_date(schaden):
	last_update_date = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return last_update_date