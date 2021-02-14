import datetime

from django import forms
from django.forms.models import inlineformset_factory

from . import models

class CustomerForm(forms.ModelForm):
	class Meta:
		model = models.Customer
		fields = '__all__'

# TODO: Both form and formset allow us to set insurance without actually creating an insurance policy. Need to fix this
class BikeForm(forms.ModelForm):
	class Meta:
		model = models.Bike
		fields = ['kunde', 'beschreibung', 'rahmennummer']

ChildFormset = inlineformset_factory(
	models.Customer, models.Bike, 
	exclude = ('insurance',), 
	extra = 1,
	can_delete = False,
	)
