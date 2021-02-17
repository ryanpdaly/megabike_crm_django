from django.db import models

from ..customers import models as customers

# Create your models here.
class ReklaTicket(models.Model):
	kunde = models.ForeignKey(customers.Customer, on_delete=models.CASCADE)
	
	STATUS_LIST = (
		('offen', 'Offen'),
		('gemeldet', 'Beim Hersteller gemeldet'),
		('eingeschickt', 'Zum Hersteller eingeschickt'),
		('wartet', 'Wartet auf bearbeitung beim Hersteller'),
		('eingetroffen', 'Ersatz eingetroffen'),
		('montage', 'Wartet auf Montage'),
		('abholbereit', 'Abholbereit'),
		('abgelehnt', 'vom Hersteller abgelehnt'),
		('erledigt', 'Erledit'),
	)
	
	status = models.CharField(
		max_length = 20,
		choices = STATUS_LIST,
		blank = False,
		)

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

	date_created = models.DateField()

	# This needs to have a list of choices
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

	class Meta:
		permissions = (
			('can_update_status', 'Can update ReklaTicket status'),
		)