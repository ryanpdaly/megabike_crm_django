import datetime

from django import forms
from django.forms.models import inlineformset_factory

from apps.customers import models

class CustomerForm(forms.ModelForm):
	class Meta:
		model = models.Customer
		fields = ['kundennummer', 'nachname']

# TODO: We should not be able to set insurance without simultaneously creating an insurance policy object from our insurance app
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
