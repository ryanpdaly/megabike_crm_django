from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from tempus_dominus.widgets import DatePicker

from apps.customers.models import Customer, Bike
import apps.insurance.models as models


# TODO: I don't like that this is hard coded
valid_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

"""
for year in range(int(datetime.now.year())-5, int(datetime.now.year())+6):
	valid_years.append(year)
"""


class CompanyForm(forms.ModelForm):
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
	class Meta:
		model = Bike
		fields = ('insurance',)


class AssonaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AssonaForm, self).__init__(*args, **kwargs)

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
	def __init__(self, *args, **kwargs):
		super(BikeleasingForm, self).__init__(*args, **kwargs)

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
	def __init__(self, *args, **kwargs):
		super(BusinessbikeForm, self).__init__(*args, **kwargs)

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
	def __init__(self, *args, **kwargs):
		super(EuroradForm, self).__init__(*args, **kwargs)

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
	class Meta:
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
		super(SchadensmeldungForm, self).__init__(*args, **kwargs)

		# Adds bootstrap styling to fields
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class SchadensmeldungStatusForm(forms.ModelForm):
	class Meta:
		model = models.SchadensmeldungStatus
		fields = ('status', 'anmerkung', 'bearbeiter')

	def __init__(self, *args, **kwargs):
		super(SchadensmeldungStatusForm, self).__init__(*args, **kwargs)

		# Adds bootstrap styling to fields
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class SchadensmeldungFileForm(forms.ModelForm):
	class Meta:
		model = models.SchadensmeldungFile
		fields = ('beschreibung', 'file', 'anmerkung', 'bearbeiter')

	def __init__(self, *args, **kwargs):
		super(SchadensmeldungFileForm, self).__init__(*args, **kwargs)

		# Adds bootstrap styling to fields
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})


class CustomStatusFormset(BaseInlineFormSet):
	def clean(self):
		for form in self.forms:
			status = form.cleaned_data.get('status')
			if not status:
				raise ValidationError('Keinen Status', 'error')

	def __init__(self, *args, **kwargs):
		super(CustomStatusFormset, self).__init__(*args, **kwargs)

		# Adds bootstrap styling to fields
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