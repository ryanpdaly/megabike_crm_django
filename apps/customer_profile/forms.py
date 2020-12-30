import datetime

import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

from .models import *

class CustomerForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('nachname', css_class='form-group col-md-4 mb-0'),
				Column('kundennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			)

class FahrzeugForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):	
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(Column('fahrzeug', css_class='form-group col-md-4 mb-0'),
				Column('rahmennummer', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
				),
			)