import datetime

from django import forms
from django.forms.models import inlineformset_factory

from apps.customers import models

class CustomerForm(forms.ModelForm):
	class Meta:
		model = models.Customer
		fields = ['kundennummer', 'nachname']

# TODO: Both form and formset allow us to set insurance without actually creating an insurance policy. Need to fix this
class BikeForm(forms.ModelForm):
	class Meta:
		model = models.Bike
		fields = ['kunde', 'beschreibung', 'rahmennummer']

BikeFormset = inlineformset_factory(
		models.Customer, models.Bike, 
		exclude = ('insurance',), 
		extra = 1,
		can_delete = False,
	)

class CustomerSearchForm(forms.ModelForm):
	class Meta:
		model = models.Customer
		fields = ['kundennummer']
		widgets = {'kundennummer':forms.NumberInput(attrs={'placeholder':'Kundennummer', 'id':'kdnr_checked'})}
