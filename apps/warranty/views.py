from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import models, forms

# Create your views here.

class TicketList(LoginRequiredMixin, generic.ListView):
	model = models.ReklaTicket
	template_name = 'warranty/list_all.html'

	#rekla_tickets = models.ReklaTicket.objects.all()

	#context = {"rekla_tickets":rekla_tickets,}

class CreateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.ReklaTicket
	permission_required = ('can_add',)

	template_name = 'warranty/new_kundenrekla.html'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm

class DisplayTicket(LoginRequiredMixin, generic.DetailView):
	model = models.ReklaTicket

	template_name_suffix = '_detail'

class UpdateTicket(LoginRequiredMixin, generic.UpdateView):
	model = models.ReklaTicket
	template_name_suffix = '_update_form'

	form_class = forms.NewTicketForm