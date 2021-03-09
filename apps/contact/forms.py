from datetime import datetime

from django import forms

from . import models

class NewPhoneContact(forms.ModelForm):
	class Meta:
		model = models.PhoneContact
		fields = ('status', 'kundenname', 'telefonnr', 'anmerkungen',)

class UpdatePhoneContactStatus(forms.ModelForm):
	class Meta:
		model = models.PhoneContact
		fields = ('status', 'anmerkungen',)