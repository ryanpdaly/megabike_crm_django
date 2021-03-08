import datetime

from django.db import models

# Create your models here.

class PhoneContact(models.Model):
	date = models.DateField()

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

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(PhoneContact, self).save()