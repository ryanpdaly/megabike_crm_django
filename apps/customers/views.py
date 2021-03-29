from django import template

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django import forms as django_forms
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from apps.customers import models
from apps.customers import forms
from apps.insurance import forms as insurance_forms
from apps.insurance import models as insurance_models
from apps.warranty import models as warranty_models

# Create your views here.

@login_required
def bike_detail_view(request, pk, rn):
	customer_instance = get_object_or_404(models.Customer, pk=pk)
	bike_instance = get_object_or_404(models.Bike, rahmennummer=rn)
	insurance = bike_instance.insurance

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
		'insurance_info':insurance_info
	}

	return render(request, 'customers/bike_detail.html', context=context)

@login_required
def bike_input_view(request, pk):
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
	}

	return render(request, 'customers/bike_input.html', context=context)

class BikeUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = models.Bike
	fields = '__all__'

	template_name_suffix = '_update'

	slug_url_kwarg = 'rn'

@login_required
def customer_detail_view(request, pk):
	customer_instance = get_object_or_404(models.Customer, pk=pk)
	bikes = models.Bike.objects.filter(kunde = pk)
	reklas = warranty_models.ReklaTicket.objects.filter(kunde = pk)

	context = {
		'customer': customer_instance,
		'bikes': bikes,
		'reklas': reklas,
	}

	return render(request, 'customers/customer_detail.html', context=context)

class CustomerInputView(LoginRequiredMixin, generic.CreateView):
	model = models.Customer
	template_name = 'customers/customer_input.html'
	success_url = reverse_lazy('customers:customer-list')

	form_class = forms.CustomerForm

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data['bikes'] = forms.BikeFormset(self.request.POST)
		else:
			data['bikes'] = forms.BikeFormset()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		bikes = context['bikes']
		self.object = form.save()
		if bikes.is_valid():
			bikes.instance = self.object
			bikes.save()
		return super().form_valid(form)

class CustomerListView(LoginRequiredMixin, generic.ListView):
	model = models.Customer
	template_name = 'customers/customer_list.html'

	register = template.Library()

	def get_context_data(self, **kwargs):
		context = super(CustomerListView, self).get_context_data(**kwargs)

		return context

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = models.Customer

	template_name_suffix = '_update'
	form_class = forms.CustomerForm