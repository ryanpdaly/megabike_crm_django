from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from tempus_dominus.widgets import DatePicker

from apps.customers.models import Customer, Bike
import apps.insurance.models as models

# FIXME: Is this form actually used anywhere?
class CompanyForm(forms.ModelForm):
	"""
	Django Modelform used to select the insurance company for a given bike
	"""

	def __init__(self, *args, **kwargs):
		super(CompanyForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		model = models.InsuranceCompanies
		fields = ['company_name']


class UpdateBikeForm(forms.ModelForm):
	"""
	Django Modelform used to add an insurance policy to a bike
	"""

	class Meta:
		model = Bike
		fields = ('insurance',)


class AssonaForm(forms.ModelForm):
	"""
	Django Modelform used to associate an AssonaInfo object with a Bike
	object
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable bootstrap styling
		"""

		super(AssonaForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			if field == 'versicherungskarte':
				self.fields[field].widget.attrs.update({
					'class': 'form-control-file'
				})
			else:
				self.fields[field].widget.attrs.update({
					'class': 'form-control'
				})

	class Meta:
		"""
		Selected fields(widget): rahmennummer, vertragsnummer, 
			beginn(DatePicker), versicherungskarte
		"""

		model = models.AssonaInfo
		fields = ('rahmennummer', 'vertragsnummer', 'beginn', 'versicherungskarte',)
		widgets = {
			'beginn': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class BikeleasingForm(forms.ModelForm):
	"""
	Django Modelform used to associate a BikeleasingInfo object with a
	Bike object
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(BikeleasingForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			if field == 'versicherungskarte':
				self.fields[field].widget.attrs.update({
					'class': 'form-control-file'
				})
			else:
				self.fields[field].widget.attrs.update({
					'class': 'form-control'
				})

	class Meta:
		"""
		Selected fields(widgets): rahmennummer, nutzer_id, paket, 
		inspektion, leasingbank, beginn(DatePicker), versicherungskarte 
		"""

		model = models.BikeleasingInfo
		fields = (
			'rahmennummer',
			'nutzer_id',
			'paket',
			'inspektion',
			'leasingbank',
			'beginn',
			'versicherungskarte'
		)
		widgets = {
			'beginn': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class BusinessbikeForm(forms.ModelForm):
	"""
	Django Modelform used to associate a BusinessbikeInfo object with a
	Bike object
	"""
	
	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(BusinessbikeForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			if field == 'versicherungskarte':
				self.fields[field].widget.attrs.update({
					'class': 'form-control-file'
				})
			else:
				self.fields[field].widget.attrs.update({
					'class': 'form-control'
				})

	class Meta:
		"""
		Selected fields(widgets): rahmennummer, beginn(DatePicket), 
			ende(DatePicker), policenummer, paket, verschleiß_guthaben,
			versicherungskarte
		"""

		model = models.BusinessbikeInfo
		fields = (
			'rahmennummer',
			'beginn',
			'ende',
			'policenummer',
			'paket',
			'verschleiss_guthaben',
			'versicherungskarte',
		)
		widgets = {
			'beginn': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			),
			'ende': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class EnraForm(forms.ModelForm):
	"""
	Django Modelform used to associate an EnraInfo object with a
		Bike object
	"""

	def __init__(self, *args, **kwargs):
		super(EnraForm, self).__init__(*args, **kwargs)

		# Adds bootstrap styling to fields
		for field in self.fields:
			if field == 'versicherungskarte':
				self.fields[field].widget.attrs.update({
					'class': 'form-control-file'
				})
			else:
				self.fields[field].widget.attrs.update({
					'class': 'form-control'
				})

	class Meta:
		model = models.EnraInfo
		fields = ('rahmennummer', 'beginn', 'policenummer', 'versicherungskarte',)
		widgets = {
			'beginn': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class EuroradForm(forms.ModelForm):
	"""
	Django Modelform used to associate an EuroradInfo form with a Bike
		object
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ that adds Bootstrap form styling
		"""

		super(EuroradForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			if field == 'versicherungskarte':
				self.fields[field].widget.attrs.update({
					'class': 'form-control-file'
				})
			else:
				self.fields[field].widget.attrs.update({
					'class': 'form-control'
				})

	class Meta:
		"""
		Included fields(widgets): rahmennummer, beginn(DatePicker),
			vertragsnummer, versicherungskarte
		"""

		model = models.EuroradInfo
		fields = ('rahmennummer', 'beginn', 'vertragsnummer', 'versicherungskarte')
		widgets = {
			'beginn': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class SchadensmeldungForm(forms.ModelForm):
	"""
	Django Modelform used to create a Schadensmeldung object
	"""

	class Meta:
		"""
		Included fields(widgets): unternehmen, schadensnummer,
			auftragsnummer, rechnungsnummer, reparatur_datum(DatePicker),
			zahlungsreferenz, bearbeiter
		"""

		model = models.Schadensmeldung
		fields = (
			'unternehmen',
			'schadensnummer',
			'auftragsnr',
			'rechnungsnr',
			'reparatur_datum',
			'zahlungsreferenz',
			'bearbeiter',
		)
		widgets = {
			'reparatur_datum': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to add Bootstrap styling to fields
		"""

		super(SchadensmeldungForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class SchadensmeldungStatusForm(forms.ModelForm):
	"""
	Django Modelform used to create SchadensmeldungStatus objects
	"""

	class Meta:
		"""
		Included fields: status, anmerkung, bearbeiter
		"""

		model = models.SchadensmeldungStatus
		fields = ('status', 'anmerkung', 'bearbeiter')

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to add Bootstrap styling to fields
		"""

		super(SchadensmeldungStatusForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class SchadensmeldungFileForm(forms.ModelForm):
	"""
	Django Modelform used to create SchadensmeldungFile objects
	"""

	class Meta:
		"""
		Included fields: beschreibung, file, anmerkung, bearbeiter
		"""

		model = models.SchadensmeldungFile
		fields = ('beschreibung', 'file', 'anmerkung', 'bearbeiter')

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(SchadensmeldungFileForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class CustomStatusFormset(BaseInlineFormSet):
	"""
	Django BaseInlineFormset used to create SchadensmeldungStatus
		objects on Schadensmeldung creation
	"""

	def clean(self):
		"""
		Custom clean method that raises ValidationError if a status is
			not selected
		"""

		for form in self.forms:
			status = form.cleaned_data.get('status')
			if not status:
				raise ValidationError('Keinen Status', 'error')

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ method that adds Bootstrap styling to all fields
		"""

		super(CustomStatusFormset, self).__init__(*args, **kwargs)

		for form in self.forms:
			for field in form.fields:
				form.fields[field].widget.attrs.update({'class': 'form-control'})


StatusFormset = inlineformset_factory(
		models.Schadensmeldung, models.SchadensmeldungStatus,
		exclude=('created', 'updated', 'date'),
		min_num=1,
		extra=0,
		can_delete=False,
		formset=CustomStatusFormset,
	)

# This is needed if we add a file form to our ticket creation form
"""
FileFormset = inlineformset_factory(
		models.Schadensmeldung, models.SchadensmeldungFile,
		exclude = ('created', 'updated', 'date'),
		min_num = 1,
		extra=0,
		can_delete = True
	)
"""