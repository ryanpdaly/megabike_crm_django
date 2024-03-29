from django import template

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django import forms as django_forms
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from apps.common import mixins as common_mixins
from apps.customers import models
from apps.customers import forms
from apps.insurance import forms as insurance_forms
from apps.insurance import models as insurance_models
from apps.warranty import models as warranty_models


# TODO: Rework this as CBV?
@login_required
def bike_detail_view(request, pk, rn):
	"""
	Function based view used to display the details of a bike object

	Parameters
	----------
	request: A Django request object
	pk: The 'kundennummer' of the customer the bike belongs to
	rn: The 'rahmennummer' of the bike
	"""

	customer_instance = get_object_or_404(models.Customer, pk=pk)
	bike_instance = get_object_or_404(models.Bike, rahmennummer=rn)
	insurance = bike_instance.insurance

	# Why is this defined here instead of in insurance app?
	INSURANCE_OPTIONS = {
		'no': 'None',
		'as': insurance_models.AssonaInfo,
		'bl': insurance_models.BikeleasingInfo,
		'bu': insurance_models.BusinessbikeInfo,
		'en': insurance_models.EnraInfo,
		'eu': insurance_models.EuroradInfo,
	}

	if bike_instance.insurance != 'no':
		insurance_info = get_object_or_404(INSURANCE_OPTIONS[insurance], rahmennummer=rn)
	else:
		insurance_info = False

	company_form = insurance_forms.CompanyForm()

	context = {
		'customer':customer_instance,
		'bike':bike_instance,
		'company_form':company_form,
		'insurance_info':insurance_info,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'customers/bike_detail.html', context=context)

# TODO: Rework this as CBV?
@login_required
def bike_input_view(request, pk):
	"""
	A function based view used to create bike objects

	Parameters
	----------
	request: A Django request object
	pk: The 'kundennummer' of the customer to whom the bike belongs
	"""

	customer_instance = get_object_or_404(models.Customer, pk=pk)

	if request.method == "POST":
		bike_form = forms.BikeForm(request.POST)

		if bike_form.is_valid():
			bike_form.save()

			return HttpResponseRedirect(reverse('customers:customer-detail', kwargs={'pk':pk}))
	else:
		bike_form = forms.BikeForm(initial={'kunde':pk})

		# TODO: Need to protect/disable the kundennummer field while still passing a value
		bike_form.fields['kunde'].widget = django_forms.HiddenInput()

	context = {
		'bike_form': bike_form,
		'customer': customer_instance,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'customers/bike_input.html', context=context)

class BikeUpdateView(LoginRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	"""
	A Django UpdateView used to update the attributes of a bike object
	"""

	model = models.Bike
	fields = '__all__'

	template_name_suffix = '_update'

	slug_url_kwarg = 'rn'

# TODO: Rework as CBV?
@login_required
def customer_detail_view(request, pk):
	"""
	A Django function based view used to display the details of a customer object
	"""

	customer_instance = get_object_or_404(models.Customer, pk=pk)
	bikes = models.Bike.objects.filter(kunde=pk)
	
	insurance_tickets = insurance_models.Schadensmeldung.objects.filter(kunde=pk)
	# Define erledigt statuses in insurance.models?
	schaden_erledigt = ['Bezahlt', 'Abgelehnt',]

	warranty_tickets = warranty_models.ReklaTicket.objects.filter(kunde=pk)
	# Define erledigt statuses in warranty.models?
	warranty_erledigt = []

	context = {
		'customer': customer_instance,
		'bikes': bikes,
		
		'insurance_tickets': insurance_tickets,
		'schaden_erledigt': schaden_erledigt, 
		
		'warranty_tickets': warranty_tickets,
		'warranty_erledigt': warranty_erledigt,

		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, 'customers/customer_detail.html', context=context)

# TODO: This does not check if customer already exists, does not handle error elequently.
class CustomerInputView(LoginRequiredMixin, generic.CreateView, common_mixins.NotificationsMixin):
	"""
	A Django CreateView used to create customer objects
	"""

	model = models.Customer
	template_name = 'customers/customer_input.html'

	form_class = forms.CustomerForm

	def form_valid(self, form):
		"""
		Custom form_valid that checks and saves forms from BikeFormset
		"""

		context = self.get_context_data()
		bikes = context['bikes']
		self.object = form.save()
		if bikes.is_valid():
			bikes.instance = self.object
			bikes.save()
		return super().form_valid(form)	


	def get_context_data(self, **kwargs):
		"""
		Custom get_context_data that adds BikeFormset to context_data 
		"""

		data = super().get_context_data(**kwargs)

		if self.request.POST:
			data['bikes'] = forms.BikeFormset(self.request.POST)
		else:
			data['bikes'] = forms.BikeFormset()
		return data

	def get_success_url(self):
		"""
		Reads the "name" attribute of the save button on the form in 
		order to forward dynamically
		"""

		# TODO: This is going to scale incredibly poorly. Figure out a better solution
		if self.request.POST.get('to_customer_list'):
			return reverse('customers:customer-list')
		elif self.request.POST.get('to_new_schaden'):
			return reverse('insurance:schaden-new')
		elif self.request.POST.get('to_new_rekla'):
			return reverse('warranty:new-ticket')
		else:
			return reverse('customers:customer-list')


class CustomerListView(LoginRequiredMixin, generic.ListView, common_mixins.NotificationsMixin):
	"""
	A Django ListView that displays a list of customer objects
	"""

	model = models.Customer
	template_name = 'customers/customer_list.html'

	# What does this even do? Why is this even here?
	register = template.Library()

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView, common_mixins.NotificationsMixin):
	"""
	A Django UpdateView used to update customer object attributes
	"""

	model = models.Customer

	template_name_suffix = '_update'
	form_class = forms.CustomerForm