from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from apps.common import mixins as common_mixins
from apps.contact import models, forms


# FIXME: Ambiguous name. Rename to IncomingCallList?
class CallList(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	"""
	A Django Listview of all incoming customer phone contacts

	Parameters
	----------

	"""

	model = models.PhoneContact
	template_name = 'contact/phonecontact_list.html'

	def get_queryset(self):
		"""
		Custom get_queryset behavior to allow filtering by status and 
			abteilung
		"""

		data = super(CallList, self).get_queryset()

		if self.kwargs.get('abteilung') == 'all':
			data = data.exclude(abteilung = 'neurad')
		else:
			data = data.filter(abteilung = self.kwargs.get('abteilung'))

		# Alternative approach: Button group with possible statuses, create list of checked buttons on page load. Check against list.
		if self.kwargs.get('filter') == 'open':
			data = data.exclude(status='erledigt')
		return data


# FIXME: Ambiguous name. Rename to IncomingCallCreate?
class CreatePhoneContact(LoginRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	A Django Createview for customer phone contacts
	"""

	model = models.PhoneContact

	template_name = 'contact/phonecontact_create.html'
	success_url = reverse_lazy('contact:call-list', kwargs={'abteilung':'all', 'filter':'open'})

	form_class = forms.NewPhoneContact


# FIXME: Ambiguous name. Rename to IncomingCallStatus or IncomingCallNewStatus
class UpdatePhoneContactStatus(LoginRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	"""
	A Django Updateview for customer phone contacts
	"""

	model = models.PhoneContact
	template_name_suffix = '_update_status'
	success_url = reverse_lazy('contact:call-list', kwargs={'abteilung':'all', 'filter':'open'})

	form_class = forms.UpdatePhoneContactStatus

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data to select ticket using pk from url
		"""

		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

class OutgoingCallList(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	"""
	A Django ListView for outgoing call objects
	"""

	model = models.OutgoingCall
	template_name = 'contact/outgoingcall_list.html'

	def get_queryset(self):
		"""
		Custom get_queryset to only show calls from the last 14 days
		"""

		data = super(OutgoingCallList, self).get_queryset()
		date_threshold = datetime.today() - timedelta(days=14)
		data = data.filter(called_on__gt=date_threshold)

		return data


class OutgoingCallCreate(LoginRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	A Django CreateView for outgoingcall objects
	"""

	model = models.OutgoingCall

	template_name = 'contact/outgoingcall_create.html'
	success_url = reverse_lazy('contact:outgoing-list',)

	form_class = forms.NewOutgoingCall


class OutgoingCallUpdate(LoginRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	"""
	A Django Updateview for outgoing call objects
	"""

	model = models.OutgoingCall
	template_name_suffix = '_update'
	success_url = reverse_lazy('contact:outgoing-list')

	form_class = forms.OutgoingCallUpdate

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data to select call using pk from url
		"""

		data = super().get_context_data(**kwargs)
		data['call_id'] = self.kwargs['pk']
		return data
