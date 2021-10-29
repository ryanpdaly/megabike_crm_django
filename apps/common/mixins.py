from datetime import date
import logging

from django.contrib.auth.models import User, Group
from django.views.generic.base import ContextMixin

from apps.contact import models as contact_models
from apps.insurance import models as insurance_models
from apps.warranty import models as warranty_models


def get_user_contact_tickets(request):
	"""
	A function used to retrieve phone contact notification data relevant to 
	user for all function based views

	Parameters
	----------
	request: A django request object

	Returns
	----------
	open_contact_tickets: A querset of open contact tickets, excluding
		those from user groups to which the user does not belong
	"""

	user_groups = request.user.groups.values_list('name', flat=True)

	# TODO: This is defined in two places, fix that
	ABTEILUNG_GROUPS = {
		'verkauf_employee':'verkauf',
		'werkstatt_employee':'werkstatt',
		'buero_employee':'buero',
	}

	open_contact_tickets = contact_models.PhoneContact.objects.filter(status='offen').exclude(abteilung='neurad')

	for key, val in ABTEILUNG_GROUPS.items():
		if key not in user_groups:
			open_contact_tickets = open_contact_tickets.exclude(abteilung=val)

	return open_contact_tickets

# FIXME: The name of this function does not suggest that it only 
#			returns a list if user belongs to proper group
def get_faellige_insurance_tickets(request):
	"""
	A function used to retrieve insurance notification data relevant to 
	user for all function based views

	Parameters
	----------
	request: A django request object

	Returns
	----------
	tickets_out: If user in insurance_responsibility group -a queryset
		containing overdue insurance tickets
	"""

	user_groups = request.user.groups.values_list('name', flat=True)
	if "insurance_responsibility" in user_groups:

		insurance_tickets = insurance_models.Schadensmeldung.objects.all()
		
		# TODO: Rename. These are not being excluded, rather included.
		insurance_tickets_excluded = []

		# This will become terribly inefficient as we get more and more tickets. Solve this with either a different search/filter method or archiving old tickets.
		for ticket in insurance_tickets:
			newest_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket).order_by('-id')[0]

			current_status = newest_status.status
			days_since_last_update = (date.today() - newest_status.date).days

			if (current_status in insurance_models.SCHADEN_STATUS_ERLEDIGT) or (days_since_last_update < 7):
				insurance_tickets_excluded.append(ticket.pk)			

		tickets_out = insurance_tickets.exclude(pk__in=insurance_tickets_excluded)

		return tickets_out

	else:
		return None

# FIXME: The name of this function does not suggest that it only 
#			returns a list if user belongs to proper group
def get_faellige_warranty_tickets(request):
	"""
	A function used to retrieve warranty notification data relevant to 
	user for all function based views

	Parameters
	----------
	request: A django request object

	Returns
	----------
	tickets_out: If user in warranty_responsibility group - a queryset
		containing overdue warranty tickets
	"""

	user_groups = request.user.groups.values_list('name', flat=True)

	if "warranty_responsibility" in user_groups:
		warranty_tickets = warranty_models.ReklaTicket.objects.all()
		tickets_excluded = []

		for ticket in warranty_tickets:
			newest_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket).order_by('-id')[0]

			current_status = newest_status.status
			days_since_last_update = (date.today() - newest_status.date).days

			if (current_status in warranty_models.REKLA_STATUS_ERLEDIGT) or (days_since_last_update < 7):
				tickets_excluded.append(ticket.pk)

		tickets_out = warranty_tickets.exclude(pk__in=tickets_excluded)

		return tickets_out

	else:
		return None

class NotificationsMixin(ContextMixin):
	"""
	A class mixin used to retrieve notification data relevant to user for all
		class based views
	"""

	def get_context_data(self, *args, **kwargs):
		"""
		A class method that adds open contact tickets, insurance tickets, warranty tickets relevant to user to view context data 
		"""

		data = super().get_context_data(*args, **kwargs)

		data['open_contact_tickets'] = self.get_user_contact_tickets()
		data['faellige_insurance_tickets'] = self.get_faellige_insurance_tickets()
		data['faellige_warranty_tickets'] = self.get_faellige_warranty_tickets()

		return data

	def get_faellige_insurance_tickets(self):
		"""
		A class method that checks if user is in the 
		insurance_responsibility group and, if so, returns a queryset 
		of open overdue tickets
		"""

		user_groups = self.request.user.groups.values_list('name', flat=True)
		if "insurance_responsibility" in user_groups:

			insurance_tickets = insurance_models.Schadensmeldung.objects.all()
			insurance_tickets_excluded = []

			# This will become terribly inefficient as we get more and 
			# more tickets. Solve this with either a different 
			# search/filter method or archiving old tickets.

			for ticket in insurance_tickets:
				newest_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket).order_by('-id')[0]

				current_status = newest_status.status
				days_since_last_update = (date.today() - newest_status.date).days

				if (current_status in insurance_models.SCHADEN_STATUS_ERLEDIGT) or (days_since_last_update < 7):
					insurance_tickets_excluded.append(ticket.pk)			

			tickets_out = insurance_tickets.exclude(pk__in=insurance_tickets_excluded)

			return tickets_out

		else:
			return None

	def get_faellige_warranty_tickets(self):
		"""
		A class method that checks if user is in the 
		warranty_responsibility user group and, if so, returns a 
		queryset of overdue warranty tickets
		"""

		user_groups = self.request.user.groups.values_list('name', flat=True)

		if "warranty_responsibility" in user_groups:
			warranty_tickets = warranty_models.ReklaTicket.objects.all()
			tickets_excluded = []

			for ticket in warranty_tickets:
				newest_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket).order_by('-id')[0]

				current_status = newest_status.status
				days_since_last_update = (date.today() - newest_status.date).days

				if (current_status in warranty_models.REKLA_STATUS_ERLEDIGT) or (days_since_last_update < 7):
					tickets_excluded.append(ticket.pk)

			tickets_out = warranty_tickets.exclude(pk__in=tickets_excluded)

			return tickets_out

		else:
			return None

	def get_user_contact_tickets(self):
		"""
		A class method that returns all open contact tickets relevant 
			to the user based on user groups
		"""

		user_groups = self.request.user.groups.values_list('name', flat=True)

		ABTEILUNG_GROUPS = {
			'verkauf_employee':'verkauf',
			'werkstatt_employee':'werkstatt',
			'buero_employee':'buero',
		}

		open_contact_tickets = contact_models.PhoneContact.objects.filter(status='offen').exclude(abteilung='neurad')

		for key, val in ABTEILUNG_GROUPS.items():
			if key not in user_groups:
				open_contact_tickets = open_contact_tickets.exclude(abteilung=val)

		return open_contact_tickets



class CustomerSearchMixin:
	"""
	A class mixin to retrieve customer information for use with our 
	customer search functionality in class based views
	"""
	def get_context_data(self, request, *args, **kwargs):
		data = super().get_context_data(request, *args, **kwargs)

		# Custom context data goes here

		return data