from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import Customer, Bike
from .forms import CustomerForm, BikeForm
from ..insurance.forms import CompanyForm

ChildFormset = inlineformset_factory(
	Customer, Bike, fields='__all__', extra=1
	)


# Create your views here.
class MainView(generic.TemplateView):
	template_name = 'customers/main.html'

class CustomerListView(generic.ListView):
	model = Customer
	template_name = 'customers/customer_list.html'

def CustomerDetailView(request, pk):
	customer_instance = get_object_or_404(Customer, pk=pk)
	bikes = Bike.objects.filter(kundennummer = pk)

	context = {
		'customer': customer_instance,
		'bikes': bikes
	}

	return render(request, 'customers/customer_detail.html', context=context)

class InputCustomer(generic.CreateView):
	model = Customer
	#form_class = CustomerForm
	template_name = 'customers/customer_input.html'
	fields = '__all__'
	success_url = reverse_lazy('customers:main')


def InputBikeView(request, pk):
	customer_instance = get_object_or_404(Customer, pk=pk)

	if request.method == "POST":
		bike_form = BikeForm(request.POST)

		if bike_form.is_valid():
			bike_form.save()

			return HttpResponseRedirect(reverse('customers:customer-detail', kwargs={'pk':pk}))

	else:
		bike_form = BikeForm(initial={'kundennummer':pk})

		# TODO: Need to protect/disable the kundennummer field while still passing a value
		bike_form.fields['kundennummer'].widget = forms.HiddenInput()

	context = {
		'bike_form': bike_form,
		'customer': customer_instance,
	}

	return render(request, 'customers/bike_input.html', context=context)

def BikeDetailView(request, pk, rn):
	customer_instance = get_object_or_404(Customer, pk=pk)
	bike_instance = get_object_or_404(Bike, rahmennummer=rn)

	company_form = CompanyForm()

	context = {
		'customer':customer_instance,
		'bike':bike_instance,
		'company_form':company_form,
	}

	return render(request, 'customers/bike_detail.html', context=context)