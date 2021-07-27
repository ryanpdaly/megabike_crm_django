from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from apps.customers.models import Customer, Bike
import apps.insurance.models as models


# TODO: I don't like that this is hard coded
valid_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
#valid_years = []

#for year in range(int(datetime.now.year())-5, int(datetime.now.year())+6):
#	valid_years.append(year)

class CompanyForm(forms.ModelForm):
	class Meta:
		model = models.InsuranceCompanies
		fields = ['company_name']

class UpdateBikeForm(forms.ModelForm):
	class Meta:
		model = Bike
		fields = ('insurance',)

class AssonaForm(forms.ModelForm):
	class Meta:
		model = models.AssonaInfo
		#fields = '__all__'
		exclude = ('id',)
		widgets = {'beginn': SelectDateWidget(years = valid_years)}

class BikeleasingForm(forms.ModelForm):
	class Meta:
		model = models.BikeleasingInfo
		fields = '__all__'
		widgets = {'beginn': SelectDateWidget(years = valid_years)}

class BusinessbikeForm(forms.ModelForm):
	class Meta:
		model = models.BusinessbikeInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years),
		 'ende':SelectDateWidget(years = valid_years), }

class EnraForm(forms.ModelForm):
	class Meta:
		model = models.EnraInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years)}

class EuroradForm(forms.ModelForm):
	class Meta:
		model = models.EuroradInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years)}

class SchadensmeldungForm(forms.ModelForm):
	class Meta:
		model = models.Schadensmeldung
		fields = ('unternehmen', 'schadensnummer', 'auftragsnr', 'rechnungsnr', 'reparatur_datum',)
		widgets = {'reparatur_datum': SelectDateWidget(years = valid_years)}

class SchadensmeldungStatusForm(forms.ModelForm):
	class Meta:
		model = models.SchadensmeldungStatus
		fields = ('status', 'anmerkung',)

class SchadensmeldungFileForm(forms.ModelForm):
	class Meta:
		model = models.SchadensmeldungFile
		fields = ('beschreibung', 'file', 'anmerkung',)

class CustomStatusFormset(BaseInlineFormSet):
	def clean(self):
		for form in self.forms:
			status = form.cleaned_data.get('status')
			if not status:
				raise ValidationError('Keinen Status', 'error')

StatusFormset = inlineformset_factory(
		models.Schadensmeldung, models.SchadensmeldungStatus,
		exclude = ('created', 'updated', 'date'),
		min_num = 1,
		extra = 0,
		can_delete = False,
		formset = CustomStatusFormset,
	)

"""
FileFormset = inlineformset_factory(
		models.Schadensmeldung, models.SchadensmeldungFile,
		exclude = ('created', 'updated', 'date'),
		min_num = 1,
		extra=0,
		can_delete = True
	)
"""