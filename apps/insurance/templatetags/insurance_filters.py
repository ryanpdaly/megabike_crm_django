import datetime
import logging

from django import template

from apps.insurance import models


register = template.Library()

@register.filter(name='insurance_current_status')
def insurance_current_status(schaden):
	return models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].get_status_display()

# TODO: Rename to days_since_last_update or something in that direction
@register.filter(name='insurance_last_update')
def insurance_last_update(schaden):
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

@register.filter(name='insurance_last_update_date')
def get_last_update_date(schaden):
	last_update_date = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return last_update_date
