from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.forms.models import inlineformset_factory
from django.urls import reverse, reverse_lazy

from .models import Customer, Bike
from .forms import CustomerForm, BikeForm

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
	#TODO: This needs pagination.

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
	template_name = 'customers/input_customer.html'
	fields = '__all__'
	success_url = reverse_lazy('customers:main')

class InputFahrzeug(generic.CreateView):
	model = Bike
	form_class = BikeForm
	template_name = 'customers/fahrzeug.html'