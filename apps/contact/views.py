from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import models, forms

# Create your views here.

class CallList(LoginRequiredMixin, generic.ListView):
	model = models.PhoneContact
	template_name = 'contact/phonecontact_list.html'

class CreatePhoneContact(LoginRequiredMixin, generic.CreateView):
	model = models.PhoneContact

	template_name = 'contact/phonecontact_create.html'
	success_url = reverse_lazy('contact:call-list')

	form_class = forms.NewPhoneContact

class UpdatePhoneContactStatus(LoginRequiredMixin, generic.UpdateView):
	model = models.PhoneContact
	template_name_suffix = '_update_status'
	success_url = reverse_lazy('contact:call-list')

	form_class = forms.UpdatePhoneContactStatus

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data