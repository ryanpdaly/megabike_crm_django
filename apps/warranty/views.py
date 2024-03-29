import datetime
import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from apps.common import mixins as common_mixins
from apps.warranty import models, forms
from apps.customers import models as customer_models
from apps.customers import forms as customer_forms


logger = logging.getLogger(__name__)


class TicketList(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	"""
	Django Listview used to display a list of ReklaTicket objects
	"""

	model = models.ReklaTicket
	template_name = 'warranty/list_all.html'

	# FIXME: Why is this called if there is no custom behavior?
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		return data


class CreateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	Django CreateView used to create ReklaTicket objects
	"""

	model = models.ReklaTicket
	permission_required = ('warranty.add_reklaticket',)

	template_name = 'warranty/new_kundenrekla.html'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data used to enable customer search functionality
		"""
		context = super().get_context_data(**kwargs)

		kdnr_input = self.request.GET.get("kdnr_input")

		if kdnr_input:
			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=kdnr_input)
		else:
			customer_options = customer_models.Customer.objects.all()

		context['customer_options'] = customer_options
		context['customer_input_forward'] = "to_new_rekla"

		return context

	def get(self, request, *args, **kwargs):
		"""
		Custom get behavior used to handle AJAX requests
		"""

		# Handles GET requests, instantiates blank form and formsets
		self.object = None

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		# TODO: rename customer_search to customer_form?
		customer_search = customer_forms.CustomerSearchForm()
		status_form = forms.StatusFormset()
		files_form = forms.FileFormset()

		if self.request.is_ajax():
			kdnr_input = request.GET.get('kdnr_input')
			self.kwargs['kdnr_input'] = kdnr_input

			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=kdnr_input)
			
			kdnr_checked = self.request.GET.get('kdnr_checked')

			if kdnr_checked:
				kdnr_checked = int(kdnr_checked)
				customer_search = customer_forms.CustomerSearchForm(initial={'kundennummer': kdnr_checked})

				if customer_models.Customer.objects.filter(kundennummer__in=customer_options).exists():
					logging.debug("Selected customer in customer options list")
					self.kwargs['kdnr_checked'] = int(kdnr_checked)
				else:
					logging.debug("Selected customer NOT in customer options list")
					self.kwargs['kdnr_checked'] = None
					kdnr_checked = None

			else:
				customer_search = customer_forms.CustomerSearchForm(initial={'kundennummer': kdnr_input})

			html = render_to_string(
				template_name="customers/customer_search_partial.html",
				context={
					"customer_options": customer_options,
					"kdnr_checked": kdnr_checked,
					"kdnr_input": kdnr_input,
					"customer_search": customer_search,
					"customer_input_forward": "to_new_rekla",
				}
			)

			data_dict = {"html_from_view": html}

			return JsonResponse(data=data_dict, safe=False)	

		return render(
			request,
			self.template_name,
			self.get_context_data(
				form=form,
				status_form=status_form,
				files_form=files_form,
				customer_search=customer_search,
			)
		)

	def post(self, request, *args, **kwargs):
		"""
		Custom post behavior used to check additional forms, formats
			dates input in forms
		"""

		# Handles POST requests, instatiates form instance and formsets with POST variables and checks validity

		# TODO: This seems janky as hell. Figure out how to do this in the regular form processing/cleaning of Django.
		post_data = request.POST.copy()
		input_date = post_data['angenommen']
		post_data['angenommen'] = datetime.datetime.strptime(input_date, '%d.%m.%Y')
		request.POST = post_data

		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		customer_search = customer_forms.CustomerSearchForm(self.request.POST, instance=form.instance)
		status_form = forms.StatusFormset(self.request.POST, instance=form.instance)
		files_form = forms.FileFormset(self.request.POST, self.request.FILES, instance=form.instance)

		# TODO: This does not check if the kdnr entered is valid
		if form.is_valid() and status_form.is_valid() and customer_search.is_valid():
			return self.form_valid(request, form, status_form, files_form, customer_search)
		else:
			return self.form_invalid(request, form, status_form, files_form, customer_search)

	# TODO: Signature of method does not match that of base class
	def form_valid(self, request, form, status_form, files_form, customer_search):
		"""
		Custom form_valid behavior used to process additional forms on page
		"""

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

	# TODO: Add customer_search to argument list?
	def form_invalid(self, request, form, status_form, files_form):
		"""
		Custom form_invalid behavior used to return input values from
			additional forms on page
		"""

		# Called if form invalid, re-renders context data with data-filled forms and errors

		return render(
			request,
			self.template_name,
			self.get_context_data(
				form=form,
				status_form=status_form,
				files_form=files_form,
			)
		)


class DisplayTicket(LoginRequiredMixin, generic.DetailView, common_mixins.NotificationsMixin):
	"""
	Django DetailView used to display details of a given ReklaTicket
		object
	"""

	model = models.ReklaTicket
	template_name_suffix = '_detail'

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data used to include past and current 
			statuses
		"""

		data = super().get_context_data(**kwargs)
		
		data['status_updates'] = models.ReklaStatusUpdate.objects.filter(rekla_ticket=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		data['files'] = models.ReklaFile.objects.filter(rekla_ticket=self.kwargs['pk'])

		return data


# TODO: Rename to be less ambiguous, maybe something like EditTicket
class UpdateTicket(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	"""
	Django UpdateView used to edit attributes of ReklaTicket objects
	"""

	model = models.ReklaTicket
	permission_required = ('warranty.add_reklaticket',)
	template_name_suffix = '_update_modal'
	success_url = reverse_lazy('warranty:main')

	form_class = forms.NewTicketForm


class AddFile(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	Django CreateView used to create ReklaFile objects
	"""

	model = models.ReklaFile
	permission_required = ('warranty.add_reklaticket',)
	fields = ('beschreibung', 'file', 'anmerkung',)

	template_name = 'warranty/add_file.html'

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data used to retrieve ticket using pk 
			keyword from URL
		"""

		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		"""
		Custom form_valid used to set rekla_ticket using pk keyword from URL
		"""

		rekla_ticket = models.ReklaTicket.objects.filter(id=self.kwargs['pk'])
		form.instance.rekla_ticket = rekla_ticket[0]

		return super().form_valid(form)


# TODO: Why doesn't this use the StatusUpdateForm created in forms?
class UpdateStatus(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	Django CreateView used to create ReklaStatusUpdate objects
	"""

	model = models.ReklaStatusUpdate
	permission_required = ('warranty.add_reklaticket',)
	fields = ('status', 'anmerkung')

	template_name = 'warranty/update_status.html'

	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data behavior used to set ReklaTicket object
			using pk keyword from URL
		"""

		data = super().get_context_data(**kwargs)
		data['ticket_id'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		"""
		Custom form_valid behavior used to set ReklaTicket object using
			pk keyword from URL
		"""

		rekla_ticket = models.ReklaTicket.objects.filter(id=self.kwargs['pk'])
		form.instance.rekla_ticket = rekla_ticket[0]
		return super().form_valid(form)


# TODO: Value pk is not used
def display_file(request, pk, sk):
	"""
	Function based view used to display files belonging to a given ReklaTicket object
	"""

	file_object = get_object_or_404(models.ReklaFile, id=sk)

	context = {
		'file_object': file_object,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'warranty/display_file.html', context=context)
