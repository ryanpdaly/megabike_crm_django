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


class CallList(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	model = models.PhoneContact
	template_name = 'contact/phonecontact_list.html'

	def get_queryset(self):
		data = super(CallList, self).get_queryset()

		if self.kwargs.get('abteilung') != 'all':
			data = data.filter(abteilung = self.kwargs.get('abteilung'))

		if self.kwargs.get('filter') == 'open':
			data = data.exclude(status='erledigt')
		return data

class CreatePhoneContact(LoginRequiredMixin, generic.CreateView):
	model = models.PhoneContact

	template_name = 'contact/phonecontact_create.html'
	success_url = reverse_lazy('contact:call-list', kwargs={'abteilung':"all", 'filter':"open"})

	form_class = forms.NewPhoneContact

class UpdatePhoneContactStatus(LoginRequiredMixin, generic.UpdateView):
	model = models.PhoneContact
	template_name_suffix = '_update_status'
	success_url = reverse_lazy('contact:call-list', kwargs={'abteilung':'all', 'filter':'open'})

	form_class = forms.UpdatePhoneContactStatus

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

class OutgoingCallList(LoginRequiredMixin, generic.ListView):
	model = models.OutgoingCall
	template_name = 'contact/outgoingcall_list.html'

	def get_queryset(self):
		data = super(OutgoingCallList, self).get_queryset()
		date_threshold = datetime.today() - timedelta(days=14)
		data = data.filter(called_on__gt=date_threshold)

		return data

class OutgoingCallCreate(LoginRequiredMixin, generic.CreateView):
	model = models.OutgoingCall

	template_name = 'contact/outgoingcall_create.html'
	success_url = reverse_lazy('contact:outgoing-list',)

	form_class = forms.NewOutgoingCall

class OutgoingCallUpdate(LoginRequiredMixin, generic.UpdateView):
	model = models.OutgoingCall
	template_name_suffix = '_update'
	success_url = reverse_lazy('contact:outgoing-list')

	form_class = forms.OutgoingCallUpdate

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['call_id'] = self.kwargs['pk']
		return data