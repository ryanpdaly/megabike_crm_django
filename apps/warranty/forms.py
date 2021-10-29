from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from tempus_dominus.widgets import DatePicker

from apps.warranty import models
from apps.customers import models as customer_models

from apps.customers import forms as customer_forms


class NewTicketForm(forms.ModelForm):
	"""
	Django Modelform used to create ReklaTicket objects
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(NewTicketForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		"""
		Included fields(widgets): sachbearbeiter, angenommen(DatePicker), 
			hersteller, artikelnr, bezeichnung, menge, auftragsnur, 
			fehlerbeschreibung
		"""

		model = models.ReklaTicket
		fields = (
			'sachbearbeiter',
			'angenommen',
			'hersteller',
			'artikelnr',
			'bezeichnung',
			'menge',
			'auftragsnr',
			'fehlerbeschreibung',
		)
		widgets = {
			'angenommen': DatePicker(
				attrs={
					'append': 'fa fa-calendar',
					'icon_toggle': True,
				},
				options={
					'format': 'DD.MM.YYYY',
				}
			)
		}


class StatusUpdateForm(forms.ModelForm):
	"""
	Django Modelform used to create ReklaStatusUpdate objects
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(StatusUpdateForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		"""
		Included fields(widgets): status, anmerkung
		"""

		model = models.ReklaStatusUpdate
		fields = ('status', 'anmerkung')


class AddReklaFile(forms.ModelForm):
	"""
	Django Modelform used to create ReklaFile objects
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(AddReklaFile, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		"""
		Included fields: beschreibung, file, anmerkung
		"""

		model = models.ReklaFile
		fields = ('beschreibung', 'file', 'anmerkung',)


class CustomStatusFormset(BaseInlineFormSet):
	"""
	Django BaseInlineFormset to include StatusUpdateForm on page 
		displaying NewTicketForm
	"""

	def __init__(self, *args, **kwargs):
		"""
		Custom __init__ behavior to enable Bootstrap form styling
		"""

		super(CustomStatusFormset, self).__init__(*args, **kwargs)

		for form in self.forms:
			for field in form.fields:
				form.fields[field].widget.attrs.update({'class': 'form-control'})

	def clean(self):
		"""
		Custom clean behavior to raise ValidationError if no status
			selected
		"""

		for form in self.forms:
			status = form.cleaned_data.get('status')
			if not status:
				raise ValidationError('Keinen Status', 'error')


# TODO: Explicitly list desired fields
StatusFormset = inlineformset_factory(
		models.ReklaTicket, models.ReklaStatusUpdate,
		exclude=('created', 'updated', 'date'),
		min_num=1,
		extra=0,
		can_delete=False,
		formset=CustomStatusFormset,
	)

# TODO: Figure out a decent way to enable bootstrap styling for this
FileFormset = inlineformset_factory(
	models.ReklaTicket, models.ReklaFile,
	exclude=('created', 'updated', 'date'),
	min_num=1,
	extra=0,
	can_delete=True
)

CustomerFormset = inlineformset_factory(
	customer_models.Customer,
	models.ReklaTicket,
	exclude=('kundenname',),
	min_num=1,
	extra=0,
	can_delete=False,
)
