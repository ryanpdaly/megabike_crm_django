from datetime import datetime

from django import forms
from django.forms import SelectDateWidget

from . import models

# TODO: I don't like that this is hard coded
valid_years = [2020, 2021]

class NewTicketForm(forms.ModelForm):
	class Meta:
		model = models.ReklaTicket
		fields = ('kunde', 'status', 'sachbearbeiter', 'date_created', 'hersteller', 'artikelnr', 
					'bezeichnung', 'menge', 'auftragsnr', 'fehlerbeschreibung',)
		widgets = {'date_created': SelectDateWidget(years = valid_years)}