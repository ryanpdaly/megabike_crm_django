from django.contrib.auth.decorators import login_required, permission_required
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

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		return data

class CreateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.ReklaTicket
	permission_required = ('can_add',)

	template_name = 'warranty/new_kundenrekla.html'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data['update'] = forms.StatusFormset(self.request.POST)
			data['files'] = forms.FileFormset(self.request.POST, self.request.FILES)
		else:
			data['update'] = forms.StatusFormset()
			data['files'] = forms.FileFormset()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		status = context['update']
		files = context['files']
		
		self.object = form.save()

		if status.is_valid():
			status.instance = self.object
			status.save()
		if files.is_valid():
			files.instance = self.object
			files.save()
		return super().form_valid(form)

class DisplayTicket(LoginRequiredMixin, generic.DetailView):
	model = models.ReklaTicket
	template_name_suffix = '_detail'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		
		data['status_updates'] = models.ReklaStatusUpdate.objects.filter(rekla_ticket=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		data['files'] = models.ReklaFile.objects.filter(rekla_ticket=self.kwargs['pk'])

		return data

class UpdateTicket(LoginRequiredMixin, generic.UpdateView):
	model = models.ReklaTicket
	template_name_suffix = '_update_form'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm

class AddFile(LoginRequiredMixin, generic.CreateView):
	model = models.ReklaFile
	fields = ('beschreibung', 'file', 'anmerkung',)

	template_name = 'warranty/add_file.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		rekla_ticket = models.ReklaTicket.objects.filter(id=self.kwargs['pk'])
		form.instance.rekla_ticket = rekla_ticket[0]

		return super().form_valid(form)

class UpdateStatus(LoginRequiredMixin, generic.CreateView):
	model = models.ReklaStatusUpdate
	fields = ('status', 'anmerkung')

	template_name = 'warranty/update_status.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		rekla_ticket = models.ReklaTicket.objects.filter(id=self.kwargs['pk'])
		form.instance.rekla_ticket = rekla_ticket[0]
		return super().form_valid(form)

def display_file(request, pk, sk):
	file_object = get_object_or_404(models.ReklaFile, id=sk)
	filename = file_object.file

	context={
		'file_object':file_object,
	}

	return render(request, 'warranty/display_file.html', context=context)