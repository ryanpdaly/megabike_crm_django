import datetime

import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

from .models import Customer, Bike

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'

class BikeForm(forms.ModelForm):
	class Meta:
		model = Bike
		fields = ['kundennummer', 'beschreibung', 'rahmennummer', 'versicherungsunternehmen']