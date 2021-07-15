import datetime
import logging

from django import template

from apps.insurance import models

register = template.Library()

@register.filter(name='get_current_status_insurance')
def get_current_status_insurance(schaden):
	return models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].get_status_display()

# Is this a fitting name? Doesn't indicate that we are only returning a date
@register.filter(name='get_last_update_insurance')
def get_last_update_insurance(schaden):
	last_update = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days

@register.filter(name='count_open_tickets_insurance')
def count_open_tickets(kdnr):
	open_tickets = 0
	erledigt = ['be', 'ab']
	
	tickets = models.Schadensmeldung.objects.filter(kunde=kdnr)
	for ticket in tickets:
		current_status = models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket.id).order_by('-id')[0].status
		logging.debug(current_status)

		if current_status not in erledigt:
			open_tickets += 1
	
	return open_tickets