import datetime

from django import forms
from django.forms.models import inlineformset_factory

from apps.customers import models

class CustomerForm(forms.ModelForm):
	"""
	Django Modelform used to create a customer object
	"""

	class Meta:
		"""
		Selected fields: kundennummer, nachname
		"""

		model = models.Customer
		fields = ['kundennummer', 'nachname']

# TODO: We should not be able to set insurance without simultaneously creating an insurance policy object from our insurance app
class BikeForm(forms.ModelForm):
	"""
	Django Modelform used to create a bike object
	"""

	class Meta:
		"""
		Selected fields: kunde (foreign key), beschreibung, rahmennummer
		"""

		model = models.Bike
		fields = ['kunde', 'beschreibung', 'rahmennummer']

BikeFormset = inlineformset_factory(
		models.Customer, models.Bike, 
		exclude = ('insurance',), 
		extra = 1,
		can_delete = False,
	)

class CustomerSearchForm(forms.ModelForm):
	"""
	Django Modelform used for our customer search functionality
	"""

	class Meta:
		"""
		Selected fields: kundennummer (NumberInput widget)
		"""

		model = models.Customer
		fields = ['kundennummer']
		widgets = {'kundennummer':forms.NumberInput(attrs={'placeholder':'Kundennummer', 'id':'kdnr_checked'})}

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ to enable Bootstrap styling of fields
		"""
		super(CustomerSearchForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
