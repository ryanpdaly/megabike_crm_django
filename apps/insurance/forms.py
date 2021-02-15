from datetime import datetime

from django import forms
from django.forms import SelectDateWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

from .models import InsuranceCompanies, AssonaInfo, BikeleasingInfo, BusinessbikeInfo, EnraInfo, EuroradInfo

from ..customers.models import Customer, Bike

# TODO: I don't like that this is hard coded
valid_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025,]
#valid_years = []

#for year in range(int(datetime.now.year())-5, int(datetime.now.year())+6):
#	valid_years.append(year)

class CompanyForm(forms.ModelForm):
	class Meta:
		model = InsuranceCompanies
		fields = ['company_name']

class UpdateBikeForm(forms.ModelForm):
	class Meta:
		model = Bike
		fields = ('insurance',)

class AssonaForm(forms.ModelForm):
	class Meta:
		model = AssonaInfo
		#fields = '__all__'
		exclude = ('id',)
		widgets = {'beginn': SelectDateWidget(years = valid_years)}

class BikeleasingForm(forms.ModelForm):
	class Meta:
		model = BikeleasingInfo
		fields = '__all__'
		widgets = {'beginn': SelectDateWidget(years = valid_years)}

class BusinessbikeForm(forms.ModelForm):
	class Meta:
		model = BusinessbikeInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years),
		 'ende':SelectDateWidget(years = valid_years), }

class EnraForm(forms.ModelForm):
	class Meta:
		model = EnraInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years)}

class EuroradForm(forms.ModelForm):
	class Meta:
		model = EuroradInfo
		fields = '__all__'
		widgets = {'beginn':SelectDateWidget(years = valid_years)}