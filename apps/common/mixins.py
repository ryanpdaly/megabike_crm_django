from datetime import date
import logging

from django.views.generic.base import ContextMixin

from apps.contact import models as contact_models
from apps.insurance import models as insurance_models
from apps.warranty import models as warranty_models


def get_open_contact_tickets():
	return contact_models.PhoneContact.objects.filter(status='offen')

def get_faellige_insurance_tickets():
	insurance_tickets = insurance_models.Schadensmeldung.objects.all()
	insurance_tickets_excluded = []

	# This will become terribly inefficient as we get more and more tickets. Solve this with either a different search/filter method or archiving old tickets.
	for ticket in insurance_tickets:
		newest_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket).order_by('-id')[0]

		current_status = newest_status.status
		days_since_last_update = (date.today() - newest_status.date).days

		if (current_status in insurance_models.SCHADEN_STATUS_ERLEDIGT) or (days_since_last_update < 6):
			insurance_tickets_excluded.append(ticket.pk)			

	tickets_out = insurance_tickets.exclude(pk__in=insurance_tickets_excluded)

	return tickets_out

def get_faellige_warranty_tickets():
	warranty_tickets = warranty_models.ReklaTicket.objects.all()
	tickets_excluded = []

	for ticket in warranty_tickets:
		newest_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket).order_by('-id')[0]

		current_status = newest_status.status
		days_since_last_update = (date.today() - newest_status.date).days

		if (current_status in warranty_models.REKLA_STATUS_ERLEDIGT) or (days_since_last_update < 6):
			tickets_excluded.append(ticket.pk)

	tickets_out = warranty_tickets.exclude(pk__in=tickets_excluded)

	return tickets_out

# A mixin to pass required context data to our class based views in order to show alerts
class NotificationsMixin(ContextMixin):
	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)

		data['open_contact_tickets'] = contact_models.PhoneContact.objects.filter(status='offen')
 
		data['faellige_insurance_tickets'] = self.get_faellige_insurance_tickets()

		data['faellige_warranty_tickets'] = self.get_faellige_warranty_tickets()

		return data

	def get_faellige_insurance_tickets(self):
		insurance_tickets = insurance_models.Schadensmeldung.objects.all()
		insurance_tickets_excluded = []

		# This will become terribly inefficient as we get more and more tickets. Solve this with either a different search/filter method or archiving old tickets.
		for ticket in insurance_tickets:
			newest_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket).order_by('-id')[0]

			current_status = newest_status.status
			days_since_last_update = (date.today() - newest_status.date).days

			if (current_status in insurance_models.SCHADEN_STATUS_ERLEDIGT) or (days_since_last_update < 6):
				insurance_tickets_excluded.append(ticket.pk)			

		tickets_out = insurance_tickets.exclude(pk__in=insurance_tickets_excluded)

		return tickets_out

	def get_faellige_warranty_tickets(self):
		warranty_tickets = warranty_models.ReklaTicket.objects.all()
		tickets_excluded = []

		for ticket in warranty_tickets:
			newest_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket).order_by('-id')[0]

			current_status = newest_status.status
			days_since_last_update = (date.today() - newest_status.date).days

			if (current_status in warranty_models.REKLA_STATUS_ERLEDIGT) or (days_since_last_update < 6):
				tickets_excluded.append(ticket.pk)

		tickets_out = warranty_tickets.exclude(pk__in=tickets_excluded)

		return tickets_out

class CustomerSearchMixin:
	def get_context_data(self, request, *args, **kwargs):
		data = super().get_context_data(request, *args, **kwargs)

		# Custom context data goes here

		return data