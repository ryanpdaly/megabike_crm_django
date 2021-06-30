import datetime

from django import template

from apps.insurance import models

register = template.Library()

@register.filter(name='get_current_status')
def get_current_status(schaden):
	return models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].get_status_display()

# Is this a fitting name? Doesn't indicate that we are only returning a date
@register.filter(name='get_last_update')
def get_last_update(schaden):
	last_update = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days