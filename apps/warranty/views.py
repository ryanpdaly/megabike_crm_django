from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from apps.warranty import models, forms
from apps.customers import models as customer_models

# Create your views here.

class TicketList(LoginRequiredMixin, generic.ListView):
	model = models.ReklaTicket
	template_name = 'warranty/list_all.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		return data

class CreateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.ReklaTicket
	permission_required = ('warranty.add_reklaticket',)

	template_name = 'warranty/new_kundenrekla.html'
	success_url = reverse_lazy('warranty:main')

	# Split this into multiple forms/formset. 1: Customer Form, 2: Warranty form, 3: Status form
	form_class = forms.NewTicketForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		url_param = self.request.GET.get("q")

		if url_param:
			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=url_param)
		else:
			customer_options = customer_models.Customer.objects.all()

		context['customer_options'] = customer_options

		return context
	

	def get(self, request, *args, **kwargs):
		# Handles GET requests, instantiates blank form and formsets
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		status_form = forms.StatusFormset()
		files_form = forms.FileFormset()
		return render(request, self.template_name,
			self.get_context_data(form = form,
									status_form = status_form,
									files_form = files_form
									)
								)

	def post(self, request, *args, **kwargs):
		# Handles POST requests, instatiates form instance and formsets with POST variables and checks validity
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		status_form = forms.StatusFormset(self.request.POST, instance=form.instance)
		files_form = forms.FileFormset(self.request.POST, self.request.FILES, instance=form.instance)
		if form.is_valid() and status_form.is_valid():
			return self.form_valid(request, form, status_form, files_form)
		else:
			return self.form_invalid(request, form, status_form, files_form)

	def form_valid(self, request, form, status_form, files_form):
		# Called if all forms valid. Creates ReklaTicket and ReklaTicketStatus instances, redirects to success url
		self.object = form.save(commit=False)
		# pre-processing for ReklaTicket goes here
		self.object.save()

		status_form = status_form.save(commit=False)
		for status in status_form:
			# pre-processing for StatusUpdate goes here
			status.save()

		if files_form.is_valid():
			files_form = files_form.save(commit=False)
			for file in files_form:
				# pre-processing for ReklaFiles goes here
				file.save()

		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, request, form, status_form, files_form):
		# Called if form invalid, re-renders context data with data-filled forms and errors

		return render(request, self.template_name, self.get_context_data(form=form,
																status_form=status_form,
																files_form=files_form,
																)
		)

class DisplayTicket(LoginRequiredMixin, generic.DetailView):
	model = models.ReklaTicket
	template_name_suffix = '_detail'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		
		data['status_updates'] = models.ReklaStatusUpdate.objects.filter(rekla_ticket=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		data['files'] = models.ReklaFile.objects.filter(rekla_ticket=self.kwargs['pk'])

		return data

class UpdateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
	model = models.ReklaTicket
	permission_required = ('warranty.add_reklaticket',)
	template_name_suffix = '_update'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm

class AddFile(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.ReklaFile
	permission_required = ('warranty.add_reklaticket',)
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

class UpdateStatus(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.ReklaStatusUpdate
	permission_required = ('warranty.add_reklaticket',)
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