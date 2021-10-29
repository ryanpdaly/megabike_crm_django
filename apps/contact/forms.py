from datetime import datetime

from django import forms

from apps.contact import models


class NewPhoneContact(forms.ModelForm):
	"""
	Django Modelform used to create a new phone contact
	"""

	class Meta:
		model = models.PhoneContact
		fields = ('status', 'abteilung', 'kundenname', 'telefonnr', 'anmerkungen', 'gesprochen_mit',)

class UpdatePhoneContactStatus(forms.ModelForm):
	"""
	Django Modelform used to update the status of a phone contact
	"""

	class Meta:
		model = models.PhoneContact
		fields = ('status', 'abteilung', 'anmerkungen',)

class NewOutgoingCall(forms.ModelForm):
	"""
	Django Modelform used to create a new outgoing call
	"""

	class Meta:
		model = models.OutgoingCall
		fields = ('auftragsnr', 'kundenname', 'telefonnr', 'anruf_von', 'anmerkungen',)

class OutgoingCallUpdate(forms.ModelForm):
	"""
	Django Modelform used to edit the comments of an outgoing call
	"""
	class Meta:
		model = models.OutgoingCall
		fields = ('anmerkungen',)