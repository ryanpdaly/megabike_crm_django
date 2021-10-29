import datetime

from django.db import models
from django.utils import timezone

from apps.common import models as common_models


class PhoneContact(models.Model):
	"""
	A Django Model for customer phone contact tickets
	"""
	
	# FIXME: Use list from common.models or from local_lists
	ABTEILUNG_OPTIONS = (
		('werkstatt', 'Werkstatt'),
		('verkauf', 'Verkauf'),
		('buero', 'Büro'),
		('neurad', 'Neuräder'),
	)

	STATUS_OPTIONS = (
		('offen', 'Offen'),
		('bearbeitung', 'In Bearbeitung'),
		('erledigt', 'Erledigt'),
	)

	date = models.DateField()

	abteilung = models.CharField(max_length=15,
		choices = ABTEILUNG_OPTIONS,
		)

	status = models.CharField(max_length=15,
		choices=STATUS_OPTIONS,
		default='offen',
		)

	kundenname = models.CharField(max_length=30,)
	telefonnr = models.CharField(max_length=20,)
	anmerkungen = models.TextField()

	# Make this integer field, change keys to integers?
	gesprochen_mit = models.CharField(max_length=32,
		choices=common_models.MITARBEITER_ALL,
	)

	def __str__(self):
		return f'{self.date}: {self.kundenname}'

	def save(self):
		"""
		A class method that sets the sets the date of creation for 
		phone contact ticket
		"""

		if not self.id:
			self.date = datetime.date.today()
		super(PhoneContact, self).save()

class OutgoingCall(models.Model):
	"""
	A Django Model representing outgoing calls
	"""
	called_on = models.DateTimeField(auto_now_add=True)

	auftragsnr = models.CharField(max_length=16,)
	kundenname = models.CharField(max_length=32,)
	telefonnr = models.CharField(max_length=20,)

	anruf_von = models.CharField(max_length=32,
		choices=common_models.MITARBEITER_ALL,)

	anmerkungen = models.TextField()

	def __str__(self):
		return f'{self.kundenname} am {self.called_on}'