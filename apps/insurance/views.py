import datetime
import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.base import ContextMixin
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from apps.common import mixins as common_mixins
from apps.contact import models as contact_models
from apps.customers import models as customer_models
from apps.customers import forms as customer_forms
from apps.insurance import forms
from apps.insurance import models
from apps.warranty import models as warranty_models


logger = logging.getLogger(__name__)


# TODO: Rework as CBV
@login_required
def input_insurance(request, rn, insurance):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	kdnr = bike_instance.kunde.kundennummer
	rn = bike_instance.rahmennummer

	insurance_dispatcher = {
		'as': forms.AssonaForm,
		'bl': forms.BikeleasingForm,
		'bu': forms.BusinessbikeForm,
		'en': forms.EnraForm,
		'eu': forms.EuroradForm,
	}

	if request.method == "POST":
		post_data = request.POST.copy()

		# Properly formats/converts input dates
		# TODO: Make this a util function in common in order to reduce repetition
		if 'beginn' in post_data:
			input_date = post_data['beginn']
			post_data['beginn'] = datetime.datetime.strptime(input_date, '%d.%m.%Y')

		if 'ende' in post_data:
			input_date = post_data['ende']
			post_data['ende'] = datetime.datetime.strptime(input_date, '%d.%m.%Y')

		request.POST = post_data

		ins_form = insurance_dispatcher[insurance](request.POST, request.FILES)

		update_bike = forms.UpdateBikeForm(request.POST, instance=bike_instance)

		if ins_form.is_valid() and update_bike.is_valid():
			ins_form.save()
			update_bike.save()

			return HttpResponseRedirect(reverse('customers:customer-detail', kwargs={'pk': kdnr}))
	else:
		ins_form = insurance_dispatcher[insurance](initial={"rahmennummer": rn})

		update_bike = forms.UpdateBikeForm(instance=bike_instance, initial={"insurance": insurance})

	context = {
		'bike': bike_instance,
		'ins_form': ins_form,
		'update_bike': update_bike,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'insurance/input_insurance.html', context=context)


# TODO: Rework as CBV
@login_required
def list_all(request):

	policies = customer_models.Bike.objects.exclude(insurance='no')

	context = {
		'policies': policies,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'insurance/list_all.html', context=context)


class InfoPage(LoginRequiredMixin, generic.base.TemplateView, common_mixins.NotificationsMixin):
	template_name = "insurance/info_page.html"

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)

		data['json_data'] = self.read_json('apps/insurance/insurance_info.json')[self.kwargs['insurance']]

		return data

	# TODO: Move to a common util file
	def read_json(self, path):
		with open(path, 'r', encoding="UTF-8") as file:
			return json.load(file)


# TODO: Rework as CBV
@login_required
def display_policy(request, rn):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	insurance = bike_instance.insurance

	insurance_options = {
		'no': 'None',
		'as': models.AssonaInfo,
		'bl': models.BikeleasingInfo,
		'bu': models.BusinessbikeInfo,
		'en': models.EnraInfo,
		'eu': models.EuroradInfo,
	}

	insurance_url = {
		'no': 'none',
		'as': 'assona',
		'bl': 'bikeleasing',
		'bu': 'businessbike',
		'en': 'enra',
		'eu': 'eurorad'
	}

	if bike_instance.insurance != 'no':
		insurance_info = get_object_or_404(insurance_options[insurance], rahmennummer=rn)
	else:
		insurance_info = False

	context = {
		'rahmennummer': rn,
		'insurance_info': insurance_info,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, f'insurance/display_{insurance_url[insurance]}.html', context=context)


# TODO: Rework as CBV
@login_required
def schaden_list(request, status, company):
	company_filters = {
		'Alle': 'all',
		'Assona': 'as',
		'Bikeleasing': 'bi',
		'Businessbike': 'bu',
		'ENRA': 'en',
		'JobRad': 'jo',
		'Lease-a-Bike': 'le',
		'Mein-Dienstrad': 'me',
		'Wertgarantie': 'we',
	}
	
	statuses = {
		'KV eingereicht': 'kv',
		'KV freigegeben': 'kvf',
		'Rechnung eingereicht': 're',
		'Abzurechnen': 'azr',
		'Bezahlt': 'be',
		'Abgelehnt': 'ab',
	}
	
	# TODO: change insurance_current_status filter to use status instead of status display,
	#  then use our erledigt_status list from insurance.models
	erledigt = ['Bezahlt', 'Abgelehnt', ]

	# TODO: Rename schaden_list, shadows function-view name
	if company != 'all':
		schaden_list = models.Schadensmeldung.objects.filter(unternehmen=company)
	else:
		schaden_list = models.Schadensmeldung.objects.all()

	if status != 'all':
		faellig_date = (datetime.datetime.today() - datetime.timedelta(days=7)).date()

		for schaden in schaden_list:
			current_status = models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0]
			is_faellig = current_status.date <= faellig_date
			is_erledigt = current_status.status in ['be', 'ab', ]

			if status == 'faellig':
				if is_erledigt is True or is_faellig is False:
					schaden_list = schaden_list.exclude(pk=schaden.pk)
			elif status == 'open' and is_erledigt is True:
				schaden_list = schaden_list.exclude(pk=schaden.pk)
			elif status != 'open' and current_status.status != status:
				schaden_list = schaden_list.exclude(pk=schaden.pk)

	context = {
		'schaden_list': schaden_list,
		'status_selected': status,
		'erledigt': erledigt,
		'statuses': statuses,

		'company_selected': company,
		'company_filters': company_filters,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, f'insurance/schadensmeldung_list.html', context=context)


"""
class SchadenList(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	model = models.Schadensmeldung
	template_name = 'schadensmeldung_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		return context
"""


class SchadenDetail(LoginRequiredMixin, generic.DetailView, common_mixins.NotificationsMixin):
	model = models.Schadensmeldung
	template_name_suffix = '_detail'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)

		data['status_updates'] = models.SchadensmeldungStatus.objects.filter(
			schadensmeldung=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		data['files'] = models.SchadensmeldungFile.objects.filter(
			schadensmeldung=self.kwargs['pk'])

		return data


# TODO: This view doesn't open the modal, seems to redirect to normal SchadenDetail
class SchadenDetailModal(LoginRequiredMixin, generic.DetailView):
	model = models.Schadensmeldung
	template = 'schadensmeldung_detail_modal.html'

	# TODO: This get_context_data is exactly the same as in SchadenDetail, create ContextMixin?
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)

		data['status_updates'] = models.SchadensmeldungStatus.objects.filter(
			schadensmeldung=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		data['files'] = models.SchadensmeldungFile.objects.filter(
			schadensmeldung=self.kwargs['pk'])

		return data


class SchadenCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	model = models.Schadensmeldung

	# TODO: Setup permissions
	permission_required = ()
	
	template_name = 'insurance/schadensmeldung_new.html'
	success_url = reverse_lazy(
		'insurance:schaden-list',
		kwargs={'status': 'open', 'company': 'all'},
	)
	form_class = forms.SchadensmeldungForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kdnr_input = self.request.GET.get("kdnr_input")

		if kdnr_input:
			customer_options = customer_models.Customer.objects.filter(
				kundennummer__icontains=kdnr_input)
		else:
			customer_options = customer_models.Customer.objects.all()

		context['customer_options'] = customer_options

		return context

	def get(self, request, *args, **kwargs):
		# Handles GET requests, instantiates blank form and formsets

		# What is this attribute declaration even doing?
		self.object = None

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		customer_search = customer_forms.CustomerSearchForm()
		status_form = forms.StatusFormset()

		if self.request.is_ajax():
			kdnr_input = self.request.GET.get('kdnr_input')
			self.kwargs['kdnr_input'] = kdnr_input

			customer_options = customer_models.Customer.objects.filter(kundennummer__icontains=kdnr_input)

			kdnr_checked = self.request.GET.get('kdnr_checked')

			if kdnr_checked:
				kdnr_checked = int(kdnr_checked)
				customer_search = customer_forms.CustomerSearchForm(
					initial={'kundennummer': kdnr_checked})
			
				if customer_models.Customer.objects.filter(kundennummer__in=customer_options).exists():
					logging.debug("Selected customer in customer options list")
					self.kwargs['kdnr_checked'] = int(kdnr_checked)
				else:
					logging.debug("Selected customer NOT in customer options list")
					self.kwargs['kdnr_checked'] = None
					kdnr_checked = None

			else:
				customer_search = customer_forms.CustomerSearchForm(
					initial={'kundennummer': kdnr_input})

			html = render_to_string(
				template_name="customers/customer_search_partial.html",
				context={
					"customer_options": customer_options,
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
									customer_search = customer_search
									#files_form = files_form
									)
								)

	def post(self, request, *args, **kwargs):
		# Handles POST requests, instantiates form instance and formsets with POST variables and checks validity
		self.object = None
		form_class = self.get_form_class()
		
		# TODO: This seems janky as hell. Figure out how to do this in the regular form processing/cleaning of Django.
		post_data = request.POST.copy()
		input_date = post_data['reparatur_datum']
		post_data['reparatur_datum'] = datetime.datetime.strptime(input_date, '%d.%m.%Y')
		request.POST = post_data

		form = self.get_form(form_class)

		customer_search = customer_forms.CustomerSearchForm(self.request.POST, instance=form.instance)
		status_form = forms.StatusFormset(self.request.POST, instance=form.instance)
		
		if form.is_valid() and status_form.is_valid() and customer_search.is_valid():
			return self.form_valid(request, form, status_form, customer_search)
		else:
			return self.form_invalid(request, form, status_form, customer_search)


	# TODO: Signature of method does not match that of ModelFormClass --> form_valid(self, form)
	def form_valid(self, request, form, status_form, customer_search):
		# Called if all forms valid. Creates Schadensmeldung and SchadensmeldungStatus instances, redirects to success url
		self.object = form.save(commit=False)
		
		# pre-processing for Schadensmeldung Ticket goes here
		self.object.kunde_id = customer_search.cleaned_data['kundennummer']
		
		self.object.save()

		status_form = status_form.save(commit=False)
		for status in status_form:
			# pre-processing for StatusUpdate goes here
			status.save()

		return HttpResponseRedirect(self.get_success_url())

	# TODO: Signature of method does not match that of FormMixin --> form_invalid(self, form)
	def form_invalid(self, request, form, status_form, files_form):
		# Called if form invalid, re-renders context data with data-filled forms and errors

		return render(request, self.template_name, self.get_context_data(form=form,
																status_form=status_form,
																)
		)


# TODO: Errors are not displayed on modal, redirects to page without any styling
class SchadenEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	model = models.Schadensmeldung
	permission_required = ()
	
	template_name_suffix = '_edit'
	
	form_class = forms.SchadensmeldungForm

	# TODO: This seems janky as hell. Figure out how to properly format date input as string within the regular processes of Django
	def post(self, request, *args, **kwargs):
		post_data = request.POST.copy()
		input_date = post_data['reparatur_datum']
		post_data['reparatur_datum'] = datetime.datetime.strptime(input_date, '%d.%m.%Y')
		request.POST = post_data

		return super(SchadenEdit, self).post(request, *args, **kwargs)

	def get_success_url(self, **kwargs):
		return reverse('insurance:schaden-detail', kwargs={'pk':self.kwargs['pk']})


class SchadenStatusUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	model = models.SchadensmeldungStatus
	permission_required = ()

	template_name = 'insurance/schadensmeldung_status_update.html'

	# TODO: Why doesn't this use the form created in insurance/forms.py?
	fields = ('status', 'anmerkung', 'bearbeiter')

	def get_success_url(self, **kwargs):
		return reverse('insurance:schaden-detail', kwargs={'pk':self.kwargs['pk']})

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['schadensmeldung'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		schaden = models.Schadensmeldung.objects.filter(id=self.kwargs['pk'])
		form.instance.schadensmeldung = schaden[0]
		return super().form_valid(form)


class SchadensmeldungAddFile(LoginRequiredMixin, generic.CreateView):
	model = models.SchadensmeldungFile

	# TODO: Why doesn't this use the form from insurance/forms.py?
	fields = ('beschreibung', 'file', 'anmerkung', 'bearbeiter')

	template_name = 'insurance/schadensmeldung_file_add.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['schaden_id'] = self.kwargs['pk']
		return data

	def form_valid(self, form):
		schadensmeldung = models.Schadensmeldung.objects.filter(id=self.kwargs['pk'])
		form.instance.schadensmeldung = schadensmeldung[0]

		return super().form_valid(form)

def display_file(request, pk, sk):
	file_object = get_object_or_404(models.SchadensmeldungFile, id=sk)

	context={
		'file_object': file_object,
	}

	return render(request, 'insurance/schadensmeldung_file_display.html', context=context)