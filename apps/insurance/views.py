from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy

from . import models
# TODO: This seems wrong, find out the right way to do this.
from ..customer_profile import models as customer_models

from . import forms

def index(request):
	return HttpResponse('Hello from Django!')

class MainView(TemplateView):
	template_name = 'insurance/main.html'
"""
class InputAssona(CreateView):
	model = AssonaInfo
	form_class = AssonaForm
	template_name = 'insurance/input_assona.html'
"""

def assona_input_view(request, rn):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	kdnr = bike_instance.kundennummer.kundennummer
	rn = bike_instance.rahmennummer
	customer_instance = get_object_or_404(customer_models.Customer, 
		kundennummer=kdnr)
	
	if request.method == "POST":
		assona_form = forms.AssonaForm(request.POST)
		update_bike = forms.UpdateBikeForm(request.POST, instance=bike_instance)

		if assona_form.is_valid() and update_bike.is_valid():
			assona_form.save()
			update_bike.save()

			return HttpResponseRedirect(reverse('customers:bike-detail', kwargs={'pk':kdnr, 'rn':rn}))

	else:
		assona_form = forms.AssonaForm(initial={"rahmennummer":rn})
		update_bike = forms.UpdateBikeForm(instance=bike_instance, initial={"versicherungsunternehmen":"as"})


	context={
		'bike':bike_instance,
		'customer':customer_instance,
		'assona_form':assona_form,
		'update_bike':update_bike,
	}

	return render(request, 'insurance/input_assona.html', context=context)

def input_insurance(request, rn, insurance):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	kdnr = bike_instance.kundennummer.kundennummer
	rn = bike_instance.rahmennummer
	customer_instance = get_object_or_404(customer_models.Customer,
		kundennummer=kdnr)

	# This will scale horribly, there absolutely has to be a better way to do this. Maybe a dictionary with {ins_code:InsForm()}?
	if request.method == "POST":
		if insurance == 'as':
			ins_form = forms.AssonaForm(request.POST)
		elif insurance == 'bl':
			ins_form = forms.BikeleasingForm(request.POST)
		elif insurance == 'bu':
			ins_form = forms.BusinessbikeForm(request.POST)
		elif insurance == 'en':
			ins_form = forms.EnraForm(request.POST)
		elif insurance == 'eu':
			ins_form = forms.EuroradForm(request.POST)

		update_bike = forms.UpdateBikeForm(request.POST, instance=bike_instance)

		if ins_form.is_valid() and update_bike.is_valid():
			ins_form.save()
			update_bike.save()

			return HttpResponseRedirect(reverse('customers:bike-detail', kwargs={'pk':kdnr, 'rn':rn}))
	else:
		if insurance == 'as':
			ins_form = forms.AssonaForm(initial={"rahmennummer":rn})
		elif insurance == 'bl':
			ins_form = forms.BikeleasingForm(initial={"rahmennummer":rn})
		elif insurance == 'bu':
			ins_form = forms.BusinessbikeForm(initial={"rahmennummer":rn})
		elif insurance == 'en':
			ins_form = forms.EnraForm(initial={"rahmennummer":rn})
		elif insurance == "eu":
			ins_form = forms.EuroradForm(initial={"rahmennummer":rn})

		# This doesn't set an initial value for versicherungsunternehmen for some reason
		update_bike = forms.UpdateBikeForm(instance=bike_instance, initial={"versicherungsunternehmen":insurance})

	context = {
		'bike':bike_instance,
		'customer':customer_instance,
		'ins_form':ins_form,
		'update_bike':update_bike,
	}

	return render(request, 'insurance/input_bikeleasing.html', context=context)