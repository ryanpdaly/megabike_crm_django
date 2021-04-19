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

class NewOutgoingCall(forms.ModelForm):
	class Meta:
		model = models.OutgoingCall
		fields = ('auftragsnr', 'kundenname', 'telefonnr', 'anruf_von', 'anmerkungen',)

class OutgoingCallUpdate(forms.ModelForm):
	class Meta:
		model = models.OutgoingCall
		fields = ('anmerkungen',)