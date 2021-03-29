from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from apps.customers import models as customer_models
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