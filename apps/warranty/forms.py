from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from . import models

# TODO: I don't like that this is hard coded
valid_years = [2020, 2021]

class NewTicketForm(forms.ModelForm):
	class Meta:
		model = models.ReklaTicket
		fields = ('kunde', 'sachbearbeiter', 'angenommen', 'hersteller', 'artikelnr', 
					'bezeichnung', 'menge', 'auftragsnr', 'fehlerbeschreibung',)
		widgets = {'angenommen': SelectDateWidget(years = valid_years)}

class StatusUpdateForm(forms.ModelForm):
	class Meta:
		model = models.ReklaStatusUpdate
		fields = ('status', 'anmerkung')

class AddReklaFile(forms.ModelForm):
	class Meta:
		model = models.ReklaFile
		fields = ('beschreibung', 'file', 'anmerkung')


class CustomStatusFormset(BaseInlineFormSet):
	def clean(self):
		for form in self.forms:
			status = form.cleaned_data.get('status')
			if not status:
				raise ValidationError('Keinen Status', 'error')

StatusFormset = inlineformset_factory(
		models.ReklaTicket, models.ReklaStatusUpdate,
		exclude = ('created', 'updated', 'date'),
		min_num = 1,
		extra = 0,
		can_delete = False,
		formset = CustomStatusFormset,
	)


FileFormset = inlineformset_factory(
		models.ReklaTicket, models.ReklaFile,
		exclude = ('created', 'updated', 'date'),
		min_num = 1,
		extra=0,
		can_delete = True
	)