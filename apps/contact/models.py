import datetime

from django.db import models

from apps.common import models as common_models

# Create your models here.

class PhoneContact(models.Model):
	date = models.DateField()

	ABTEILUNG_OPTIONS = (
		('werkstatt', 'Werkstatt'),
		('verkauf', 'Verkauf'),
		('buero', 'Büro'),
	)

	abteilung = models.CharField(max_length=15,
		choices = ABTEILUNG_OPTIONS,
	)

	STATUS_OPTIONS = (
		('offen', 'Offen'),
		('bearbeitung', 'In Bearbeitung'),
		('erledigt', 'Erledigt'),
	)

	status = models.CharField(max_length=15,
		choices=STATUS_OPTIONS,
		default='offen',
	)

	kundenname = models.CharField(max_length=30,)
	telefonnr = models.CharField(max_length=20,)
	anmerkungen = models.TextField()

	gesprochen_mit = models.CharField(max_length=32,
		choices = common_models.MITARBEITER_ALL,
	)

	def __str__(self):
		return f'{self.date}: {self.kundenname}'

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(PhoneContact, self).save()