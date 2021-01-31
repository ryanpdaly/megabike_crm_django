#from django.forms import ModelForm, SelectDateWidget
import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

from .models import InsuranceCompanies, AssonaInfo, BikeleasingInfo, BusinessbikeInfo, EnraInfo, EuroradInfo

from ..customer_profile.models import Customer, Bike

class CompanyForm(forms.ModelForm):
	class Meta:
		model = InsuranceCompanies
		fields = '__all__'
		
#TODO: All forms require the same basic customer info, maybe have a separate CustomerForm and combine that with our <Insurance>Form
class AssonaForm(forms.ModelForm):
	class Meta:
		model = AssonaInfo
		fields = '__all__'

	'''
	beginn = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, datetime.date.today().year+1), ))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('vertragsnummer', css_class='form-group col-md-2 mb-0'),
				MultiWidgetField('beginn', css_class='form-group col-md-2 mb-0',
					attrs={'style':'width: 33%; display: inline-block;'}),
				css_class='form-row'
				),
			Submit('submit', 'Speichern')
			)

	def save(self, commit=True):
		new_kundennummer = KundenProfile.objects.filter('kundennummer')
		new_rahmennummer = FahrzeugProfile.objects.filter('rahmennummer')
		if new_kundennummer.exists():
			# Save to kundennummer
		else:
			# Create and save new customer, save 
	'''

	class Meta:
		model = AssonaInfo
		fields = '__all__'

class BikeleasingForm(forms.ModelForm):
	#TODO: No need to save this in both models.py and forms.py
	PAKET = [('P', 'Premium'), ('P+', 'Premium Plus')]
	BANKS = [('ALS', 'ALS Leasing GmbH'), ('Hofmann', 'Hofmann Leasing GmbH'),
				('Digital Mobility', 'Digital Mobility Leasing GmbH')]

	beginn = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, datetime.date.today().year+1), ))
	paket = forms.ChoiceField(choices=PAKET)
	bank = forms.ChoiceField(choices=BANKS)

	class Meta:
		model = BikeleasingInfo
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('nutzer_id', css_class='form-group col-md-2 mb-0'),
				Column('paket', css_class='form-group col-md-2 mb-0'),
				Column('inspektion', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Submit('submit', 'Speichern')
		)

class BusinessbikeForm(forms.ModelForm):
	beginn = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.date.today().year-4, datetime.date.today().year+1), ))
	ende = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.date.today().year+1, datetime.date.today().year+4)))

	class Meta:
		model = BusinessbikeInfo
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			#TODO: These two widgets should have a bit of space between them
			Row(MultiWidgetField('beginn', css_class='form-group col-md-2 mb-0',
					attrs={'style':'width: 33%; display: inline-block;'}),
				MultiWidgetField('ende', css_class='form-group col-md-2 mb-0',
					attrs={'style':'width: 33%; display: inline-block;'}),
				),
			Row(Column('paket', css_class='form-group col-md-4 mb-0'),
				),
			)

class EnraForm(forms.ModelForm):
	beginn = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.date.today().year-6, datetime.date.today().year+1), ))

	class Meta:
		model = EnraInfo
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('policenummer', css_class='form-group col-md-4 mb-0'),
				MultiWidgetField('beginn', css_class='form-group col-md-2 mb-0',
					attrs={'style':'width: 33%; display: inline-block;'}),
				),
			)

class EuroradForm(forms.ModelForm):
	beginn = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.date.today().year-6, datetime.date.today().year+1), ))

	class Meta:
		model = EuroradInfo
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			Row(Column('vertragsnummer', css_class='form-group col-md-4 mb-0'),
				MultiWidgetField('beginn', css_class='form-group col-md-2 mb-0',
					attrs={'style':'width: 33%; display: inline-block;'}),
				),
			)