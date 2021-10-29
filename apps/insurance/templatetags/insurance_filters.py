import datetime
import logging

from django import template

from apps.insurance import models


register = template.Library()

@register.filter(name='insurance_current_status')
def insurance_current_status(schaden):
	"""
	Custom Django Templatetag that returns the current status of a 
	given insurance ticket

	Parameters
	----------
	schaden: A Schadensmeldung object
	"""

	return models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].get_status_display()


# FIXME: Rename to days_since_last_update or something in that direction
@register.filter(name='insurance_last_update')
def insurance_last_update(schaden):
	"""
	Custom Django Templatetag that returns the number of days since the
	last update to a given insurance ticket

	Parameters
	----------
	schaden: A Schadensmeldung object
	"""

	last_update = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return (datetime.date.today() - last_update).days


@register.filter(name='count_open_tickets_insurance')
def count_open_tickets(kdnr):
	"""
	Custom Django Templatetag that returns the number of open tickets for a given customer

	Parameters
	----------
	kdnr: The kdnr attribute of a Customer object
	"""

	open_tickets = 0

	# FIXME: this list is located in defined in several places each
	# 		time it is used
	erledigt = ['be', 'ab']
	
	tickets = models.Schadensmeldung.objects.filter(kunde=kdnr)
	for ticket in tickets:
		current_status = models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket.id).order_by('-id')[0].status
		logging.debug(current_status)

		if current_status not in erledigt:
			open_tickets += 1
	
	return open_tickets

# FIXME: This filter isn't very flexible. Why not just return the last
#		Update object and display the date?
@register.filter(name='insurance_last_update_date')
def get_last_update_date(schaden):
	"""
	Custom Django Templatetage that returns the creation date of the
	last SchadensmeldungStatus object related to a Schadensmeldung object
	"""

	last_update_date = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0].date

	return last_update_date
