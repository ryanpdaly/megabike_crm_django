import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from apps.customers import models as customer_models
from apps.customers import forms as customer_forms
from apps.insurance import forms
from apps.insurance import models


@login_required
def input_insurance(request, rn, insurance):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	kdnr = bike_instance.kunde.kundennummer
	rn = bike_instance.rahmennummer

	INSURANCE_DISPATCHER = {
		'as':forms.AssonaForm,
		'bl':forms.BikeleasingForm,
		'bu':forms.BusinessbikeForm,
		'en':forms.EnraForm,
		'eu':forms.EuroradForm,	
	}

	if request.method == "POST":
		ins_form = INSURANCE_DISPATCHER[insurance](request.POST, request.FILES)

		update_bike = forms.UpdateBikeForm(request.POST, instance=bike_instance)

		if ins_form.is_valid() and update_bike.is_valid():
			ins_form.save()
			update_bike.save()

			return HttpResponseRedirect(reverse('customers:customer-detail', kwargs={'pk':kdnr,}))
	else:
		ins_form = INSURANCE_DISPATCHER[insurance](initial={"rahmennummer":rn})

		update_bike = forms.UpdateBikeForm(instance=bike_instance, initial={"insurance":insurance})

	context = {
		'bike':bike_instance,
		'ins_form':ins_form,
		'update_bike':update_bike,
	}

	return render(request, 'insurance/input_insurance.html', context=context)

@login_required
def list_all(request):

	policies = customer_models.Bike.objects.exclude(insurance='no')

	context = {
		'policies':policies
	}

	return render(request, 'insurance/list_all.html', context=context)

@login_required
def info_page(request, insurance):
	return render(request, f'insurance/info_{insurance}.html')

@login_required
def display_policy(request, rn):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	insurance = bike_instance.insurance

	INSURANCE_OPTIONS = {
		'no': 'None',
		'as': models.AssonaInfo,
		'bl': models.BikeleasingInfo,
		'bu': models.BusinessbikeInfo,
		'en': models.EnraInfo,
		'eu': models.EuroradInfo,
	}

	INSURANCE_URL = {
		'no':'none',
		'as':'assona',
		'bl':'bikeleasing',
		'bu':'businessbike',
		'en':'enra',
		'eu':'eurorad'
	}

	if bike_instance.insurance != 'no':
		insurance_info = get_object_or_404(INSURANCE_OPTIONS[insurance], rahmennummer=rn)
	else:
		insurance_info = False

	context = {
		'rahmennummer': rn,
		'insurance_info': insurance_info,
	}

	return render(request, f'insurance/display_{INSURANCE_URL[insurance]}.html', context=context)

@login_required
def schaden_list(request):

	schaden_list = models.Schadensmeldung.objects.all()

	context = {
		'schaden_list': schaden_list,
	}

	return render(request, f'insurance/schadensmeldung_list.html', context=context)

class SchadenDetail(LoginRequiredMixin, generic.DetailView):
	model = models.Schadensmeldung
	template_name_suffix = '_detail'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		
		data['status_updates'] = models.SchadensmeldungStatus.objects.filter(schadensmeldung=self.kwargs['pk']).order_by('-id')
		data['current_status'] = data['status_updates'][0]

		# Not currently planning on adding support for files
		#data['files'] = models.ReklaFile.objects.filter(rekla_ticket=self.kwargs['pk'])

		return data

class SchadenCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.Schadensmeldung
	permission_required = ('insurance.edit_schaden')
	
	template_name = 'insurance/schadensmeldung_new.html'
	success_url = reverse_lazy('insurance:schaden-list')

	form_class = forms.SchadensmeldungForm

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

		customer_search = customer_forms.CustomerSearchForm()
		status_form = forms.StatusFormset()

		if self.request.is_ajax():
			kdnr_input = self.request.GET.get('kdnr_input')
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
									customer_search = customer_search
									#files_form = files_form
									)
								)

	def post(self, request, *args, **kwargs):
		# Handles POST requests, instatiates form instance and formsets with POST variables and checks validity
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		customer_search = customer_forms.CustomerSearchForm(self.request.POST, instance=form.instance)
		status_form = forms.StatusFormset(self.request.POST, instance=form.instance)
		
		if form.is_valid() and status_form.is_valid() and customer_search.is_valid():
			return self.form_valid(request, form, status_form, customer_search)
		else:
			return self.form_invalid(request, form, status_form, customer_search)

	def form_valid(self, request, form, status_form, customer_search):
		# Called if all forms valid. Creates ReklaTicket and ReklaTicketStatus instances, redirects to success url
		self.object = form.save(commit=False)
		
		# pre-processing for ReklaTicket goes here
		self.object.kunde_id = customer_search.cleaned_data['kundennummer']
		
		self.object.save()

		status_form = status_form.save(commit=False)
		for status in status_form:
			# pre-processing for StatusUpdate goes here
			status.save()

		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, request, form, status_form, files_form):
		# Called if form invalid, re-renders context data with data-filled forms and errors

		return render(request, self.template_name, self.get_context_data(form=form,
																status_form=status_form,
																)
		)

class SchadenEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
	model = models.Schadensmeldung
	permission_required = ('insurance.edit_schaden',)
	
	template_name_suffix = '_edit'
	
	form_class = forms.SchadensmeldungForm

	def get_success_url(self, **kwargs):
		return reverse('insurance:schaden-detail', kwargs={'pk':self.kwargs['pk']})

class SchadenStatusUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	model = models.SchadensmeldungStatus
	permission_required = ('insurance.edit_schaden')

	template_name = 'insurance/schadensmeldung_status_update.html'

	fields = ('status', 'anmerkung',)

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