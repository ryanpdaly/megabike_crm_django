import datetime
import os
from uuid import uuid4

from django.db import models
from django.urls import reverse, reverse_lazy

from apps.customers import models as customers

def set_path_and_rename(instance, filename):
	ext = filename.split('.')[-1]
	filename = f'kd{instance.rekla_ticket.kunde.kundennummer}/{uuid4()}.{ext}'

	return filename

REKLA_STATUS_ERLEDIGT = ['erledigt']

class ReklaTicket(models.Model):
	kunde = models.ForeignKey(customers.Customer, on_delete=models.CASCADE)

	#TODO: This needs to be set one time, not in each individual apps models
	MITARBEITER_LIST = (
		('12', 'Beskowski'),
		('34', 'Wegener'),
		('59', 'Daly'),
		('61', 'Betke'),
		('65', 'Bachmann'),
		('68', 'Duhme'),
		('70', 'Nolte'),
		('72', 'Korpilla'),
	)

	sachbearbeiter = models.CharField(
		max_length = 2,
		choices = MITARBEITER_LIST,
		blank = False,
		)

	angenommen = models.DateField()
	created = models.DateField()
	updated = models.DateField()

	HERSTELLER_CHOICES = (
		('absolut', 'Absolut'),
		('abus', 'Abus'),
		('alpina', 'Alpina'),
		('asista', 'Asista'),
		('bergamont', 'Bergamont'),
		('bosch', 'Bosch'),
		('cosmic', 'Cosmic'),
		('cube', 'Cube'),
		('ergotec', 'Ergotec'),
		('grofa', 'Grofa'),
		('hamax', 'Hamax'),
		('hartje', 'Hartje'),
		('magura', 'Magura'),
		('mcg', 'MCG'),
		('new wave', 'New Wave'),
		('oneal', "O'neal"),
		('ortlieb', 'Ortlieb'),
		('lange', 'Paul Lange'),
		('puky', 'Puky'),
		('rm', 'R&M'),
		('roeckl', 'Roeckl'),
		('rti', 'RIT'),
		('sks', 'SKS'),
		('sonstige', 'Sonstige'),
		('sqlab','SQ-Lab'),
		('sram', 'SRAM DSD'),
		('supernova', 'Supernova'),
		('trek', 'Trek'),
		('trelock', 'Trelock'),
		('vaude', 'Vaude'),
		('wiener', 'Wiender'),
		('zeg', 'ZEG')
	)

	hersteller = models.CharField(max_length = 30, choices = HERSTELLER_CHOICES,)
	artikelnr = models.CharField(max_length = 30,)
	bezeichnung = models.CharField(max_length = 50,)
	menge = models.IntegerField()
	auftragsnr = models.CharField(max_length = 10,)

	fehlerbeschreibung = models.TextField()

	def __str__(self):
		return f'Ticket #{self.id}: {self.hersteller}'

	def save(self):
		if not self.id:
			self.created = datetime.date.today()
		self.updated = datetime.datetime.today()
		super(ReklaTicket, self).save()

	class Meta:
		permissions = (
		)

class ReklaStatusUpdate(models.Model):
	rekla_ticket = models.ForeignKey(ReklaTicket, on_delete = models.CASCADE)
	date = models.DateField()

	STATUS_LIST = (
		('offen', 'Offen'),
		('gemeldet', 'Beim Hersteller gemeldet'),
		('eingeschickt', 'Zum Hersteller eingeschickt'),
		('wartet', 'Wartet auf bearbeitung beim Hersteller'),
		('eingetroffen', 'Ersatz eingetroffen'),
		('montage', 'Wartet auf Montage'),
		('abholbereit', 'Abholbereit'),
		('abgelehnt', 'vom Hersteller abgelehnt'),
		('erledigt', 'Erledigt'),
	)

	status = models.CharField(max_length = 20, choices = STATUS_LIST,)
	anmerkung = models.TextField(blank=True)

	def __str__(self):
		return f'Ticket #{self.rekla_ticket.id} - {self.status} am {self.date}'

	def get_absolute_url(self):
		return reverse('warranty:display-ticket', args=(self.rekla_ticket.id,))

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(ReklaStatusUpdate, self).save()

class ReklaFile(models.Model):
	rekla_ticket = models.ForeignKey(ReklaTicket, on_delete = models.CASCADE)
	date = models.DateField()

	beschreibung = models.CharField(max_length=30)
	file = models.FileField(upload_to=set_path_and_rename)
	anmerkung = models.TextField(blank=True)

	def __str__(self):
		return f'Ticket #{self.rekla_ticket.id}: {self.beschreibung}'

	def get_absolute_url(self):
		return reverse('warranty:display-ticket', args=(self.rekla_ticket.id,))

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(ReklaFile, self).save()