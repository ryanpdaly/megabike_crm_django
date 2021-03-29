from datetime import datetime

from django import forms

from apps.contact import models

class NewPhoneContact(forms.ModelForm):
	class Meta:
		model = models.PhoneContact
		fields = ('status', 'abteilung', 'kundenname', 'telefonnr', 'anmerkungen', 'gesprochen_mit',)

class UpdatePhoneContactStatus(forms.ModelForm):
	class Meta:
		model = models.PhoneContact
		fields = ('status', 'abteilung', 'anmerkungen',)