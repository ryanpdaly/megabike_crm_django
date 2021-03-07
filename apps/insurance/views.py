from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import models
# TODO: This seems wrong, find out the right way to do this.
from ..customers import models as customer_models

from . import forms

@login_required
def input_insurance(request, rn, insurance):
	bike_instance = get_object_or_404(customer_models.Bike, rahmennummer=rn)
	kdnr = bike_instance.kunde.kundennummer
	rn = bike_instance.rahmennummer

	# This will scale horribly, there absolutely has to be a better way to do this. Maybe a dictionary with {ins_code:InsForm()}?
	if request.method == "POST":
		if insurance == 'as':
			ins_form = forms.AssonaForm(request.POST, request.FILES)
		elif insurance == 'bl':
			ins_form = forms.BikeleasingForm(request.POST, request.FILES)
		elif insurance == 'bu':
			ins_form = forms.BusinessbikeForm(request.POST, request.FILES)
		elif insurance == 'en':
			ins_form = forms.EnraForm(request.POST, request.FILES)
		elif insurance == 'eu':
			ins_form = forms.EuroradForm(request.POST, request.FILES)

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