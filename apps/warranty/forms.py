from datetime import datetime

from django import forms
from django.forms import SelectDateWidget
from django.forms.models import inlineformset_factory

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


StatusFormset = inlineformset_factory(
		models.ReklaTicket, models.ReklaStatusUpdate,
		exclude = ('created', 'updated', 'date'),
		extra = 1,
		can_delete = False
	)

FileFormset = inlineformset_factory(
		models.ReklaTicket, models.ReklaFile,
		exclude = ('created', 'updated', 'date'),
		extra = 1,
		can_delete = True
	)