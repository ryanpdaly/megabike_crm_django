import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from apps.warranty import models, forms
from apps.customers import models as customer_models
from apps.customers import forms as customer_forms

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

	form_class = forms.NewTicketForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kdnr_input = self.request.GET.get("kdnr_input")

		if kdnr_input:
			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=kdnr_input)
		else:
			customer_options = customer_models.Customer.objects.all()

		context['customer_options'] = customer_options

		return context

	def get(self, request, *args, **kwargs):
		# Handles GET requests, instantiates blank form and formsets
		self.object = None

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		# Inconsistency: rename customer_search to customer_form?
		customer_search = customer_forms.CustomerSearchForm()
		status_form = forms.StatusFormset()
		files_form = forms.FileFormset()

		# Set und call order for kdnr_input + kdnr_checked is wrong. Weird behavior when checking new kdnr with old still in search box
		if self.request.is_ajax():
			kdnr_input = request.GET.get('kdnr_input')
			self.kwargs['kdnr_input'] = kdnr_input

			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=kdnr_input)
			
			kdnr_checked = self.request.GET.get('kdnr_checked')

			if kdnr_checked:
				kdnr_checked = int(kdnr_checked)
				customer_search = customer_forms.CustomerSearchForm(initial={'kundennummer':kdnr_checked})

				if customer_models.Customer.objects.filter(kundennummer__in=customer_options).exists():
					logging.debug("Selected customer in customer options list")
					self.kwargs['kdnr_checked'] = int(kdnr_checked)
				else:
					logging.debug("Selected customer NOT in customer options list")
					self.kwargs['kdnr_checked'] = None
					kdnr_checked=None

			else:
				customer_search = customer_forms.CustomerSearchForm(initial={'kundennummer':kdnr_input})

			html = render_to_string(
				template_name="customers/customer_search_partial.html",
				context={"customer_options": customer_options,
							"kdnr_checked": kdnr_checked,
							"kdnr_input": kdnr_input,
							"customer_search": customer_search,
						}
			)

			data_dict = {"html_from_view": html}

			return JsonResponse(data=data_dict, safe=False)	

		return render(request, self.template_name,
			self.get_context_data(form = form,
									status_form = status_form,
									files_form = files_form,
									customer_search = customer_search,
									)
								)

	def post(self, request, *args, **kwargs):
		# Handles POST requests, instatiates form instance and formsets with POST variables and checks validity
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		customer_search = customer_forms.CustomerSearchForm(self.request.POST, instance=form.instance)
		status_form = forms.StatusFormset(self.request.POST, instance=form.instance)
		files_form = forms.FileFormset(self.request.POST, self.request.FILES, instance=form.instance)
		

		# This does not check if the kdnr entered is valid
		if form.is_valid() and status_form.is_valid() and customer_search.is_valid():
			return self.form_valid(request, form, status_form, files_form, customer_search)
		else:
			return self.form_invalid(request, form, status_form, files_form, customer_search)

	def form_valid(self, request, form, status_form, files_form, customer_search):
		# Called if all forms valid. Creates ReklaTicket and ReklaTicketStatus instances, redirects to success url
		self.object = form.save(commit=False)
		
		# pre-processing for ReklaTicket goes here
		self.object.kunde_id = customer_search.cleaned_data['kundennummer']
		
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
	template_name_suffix = '_update_modal'
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