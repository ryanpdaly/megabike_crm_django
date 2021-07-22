import datetime
import os
from uuid import uuid4

from django.db import models
from django.urls import reverse, reverse_lazy

from apps.customers import models as customer_models

def set_upload_path(bike, filename):
	#TODO: can't delete this because it's used in a migration. Fix that.
	pass

def set_path_and_rename(instance, filename):
	ext = filename.split('.')[-1]
	filename = f'kd{instance.rahmennummer.kunde.kundennummer}/versicherungskarten/{uuid4()}.{ext}'

	return filename

# Rework, combine with other set_path_and_rename?
def set_schadenfile_path_and_name(instance, filename):
	ext = filename.split('.')[-1]
	
	kdnr = instance.schadensmeldung.kunde.kundennummer
	unternehmen = instance.schadensmeldung.unternehmen
	schadensnr = instance.schadensmeldung.schadensnummer

	filename = f'kd{kdnr}/{unternehmen}{schadensnr}/{uuid4()}.{ext}'

	return filename

class InsuranceCompanies(models.Model):
	COMPANIES = (
		('no', 'None'),
		('as', 'Assona'),
		('bl', 'Bikeleasing Service'),
		('bu', 'Businessbike'),
		('en', 'ENRA'),
		('eu', 'Eurorad'),
	)
	
	company_name = models.CharField(max_length=2, 
		default='no', 
		choices=COMPANIES,
		)
	
	def __str__(self):
		return 'Insurance Company'

class AssonaInfo(models.Model):
	rahmennummer = models.ForeignKey(customer_models.Bike, on_delete=models.CASCADE, to_field='rahmennummer')
	vertragsnummer = models.CharField(max_length=10)
	beginn = models.DateField()

	versicherungskarte = models.FileField(blank=True, 
		upload_to=set_path_and_rename,
		)

	def __str__(self):
		return f'{self.rahmennummer} Assona'

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in AssonaInfo._meta.fields]

class BikeleasingInfo(models.Model):
	PAKET_OPTIONS = [('P', 'Premium'), ('P+', 'Premium Plus')]
	BANK_OPTIONS = [('A', 'ALS Leasing GmbH'), ('H', 'Hofmann Leasing GmbH'),
				('D', 'Digital Mobility Leasing GmbH')]

	rahmennummer = models.ForeignKey(customer_models.Bike, on_delete=models.CASCADE, to_field='rahmennummer')

	nutzer_id = models.CharField(max_length=20)
	paket = models.CharField(max_length=20, choices=PAKET_OPTIONS)
	inspektion = models.BooleanField()
	leasingbank = models.CharField(max_length=1, choices=BANK_OPTIONS)
	beginn = models.DateField()

	versicherungskarte = models.FileField(blank=True, 
		upload_to=set_path_and_rename,
		)

	def __str__(self):
		return f'Bikeleasing: {self.get_paket_display()}'
		#{self.get_paket_display} -> Throws a recursion error? Need to see display though

	def get_fields(self):
		# This needs to show display for our choice fields
		return [(field.name, field.value_from_object(self)) for field in BikeleasingInfo._meta.fields]

class BusinessbikeInfo(models.Model):
	PAKET_OPTIONS = (
		('D','Durchsicht'),
		('I', 'Inspektion'),
		('F', 'Full Service'),
		('E', 'Instandhaltungs+ enthalten'),
		('N', 'Instandhaltungs+ nicht enthalten'),
	)

	rahmennummer = models.ForeignKey(customer_models.Bike, on_delete=models.CASCADE, to_field='rahmennummer')

	beginn = models.DateField()
	ende = models.DateField()
	policenummer = models.CharField(max_length=30)
	paket = models.CharField(max_length=30, choices=PAKET_OPTIONS)
	verschleiss_guthaben = models.BooleanField(default=False)

	versicherungskarte = models.FileField(blank=True, 
		upload_to=set_path_and_rename,
		)

	def __str__(self):
		return f'Businessbike {self.get_paket_display()}'

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in BusinessbikeInfo._meta.fields]

class EnraInfo(models.Model):
	rahmennummer = models.ForeignKey(customer_models.Bike, on_delete=models.CASCADE, to_field='rahmennummer')

	beginn = models.DateField()
	policenummer = models.CharField(max_length=20)

	versicherungskarte = models.FileField(blank=True, 
		upload_to=set_path_and_rename,
		)

	def __str__(self):
		return 'ENRA'

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in EnraInfo._meta.fields]

class EuroradInfo(models.Model):
	rahmennummer = models.ForeignKey(customer_models.Bike, on_delete=models.CASCADE, to_field='rahmennummer')

	beginn = models.DateField()
	vertragsnummer = models.CharField(max_length=20)

	versicherungskarte = models.FileField(blank=True, 
		upload_to=set_path_and_rename,
		)

	def __str__(self):
		return 'Eurorad'

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in EuroradInfo._meta.fields]


SCHADEN_STATUS_ERLEDIGT = ['be', 'ab',]

# Rename to schaden? Name unneccesarily long
class Schadensmeldung(models.Model):
	kunde = models.ForeignKey(customer_models.Customer, on_delete=models.CASCADE)

	COMPANIES = (
		('as', 'Assona'),
		('bi', 'Bikeleasing-Service'),
		('bu', 'Businessbike'),
		('en', 'ENRA'),
		('jo', 'JobRad'),
		('le', 'Lease-a-Bike'),
		('me', 'Mein-Dienstrad'),
		('we', 'Wertgarantie'),
		)

	unternehmen = models.CharField(max_length=3,
									choices = COMPANIES
								)
	# Inconsistency: either all fields nr or all fields nummer
	schadensnummer = models.CharField(max_length = 30)

	auftragsnr = models.CharField(max_length = 10)
	rechnungsnr = models.CharField(max_length = 10, blank=True, null=True)
	reparatur_datum = models.DateField(blank=True, null=True)

	created = models.DateField()
	updated = models.DateField()

	def __str__(self):
		return f'{self.kunde.kundennummer}: {self.kunde.nachname} - {self.unternehmen} {self.schadensnummer}'

	def save(self):
		if not self.id:
			self.created = datetime.date.today()
		self.updated = datetime.datetime.today()
		super(Schadensmeldung, self).save()


# Rename to SchadensStatus, name unecessarily long.
class SchadensmeldungStatus(models.Model):
	schadensmeldung = models.ForeignKey(Schadensmeldung, on_delete=models.CASCADE)

	date = models.DateField()

	STATUS_LIST = (
		('kv', 'KV eingereicht'),
		('kvf', 'KV freigegeben'),
		('re', 'Rechnung eingereicht'),
		('be', 'Bezahlt'),
		('ab', 'Abgelehnt'),
		)

	status = models.CharField(max_length=3, 
								choices = STATUS_LIST
							)

	anmerkung = models.TextField(blank=True)

	def __str__(self):
		return f'Update am {self.date} zur {self.schadensmeldung.unternehmen} {self.schadensmeldung.schadensnummer}'

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(SchadensmeldungStatus, self).save()

class SchadensmeldungFile(models.Model):
	schadensmeldung = models.ForeignKey(Schadensmeldung, on_delete=models.CASCADE)
	date = models.DateField()

	beschreibung = models.CharField(max_length=30)
	file = models.FileField(upload_to=set_schadenfile_path_and_name)
	anmerkung = models.TextField(blank=True)

	def __str__(self):
		return f'{self.schadensmeldung.unternehmen} {self.schadensmeldung.schadensnummer}: {self.beschreibung}'

	def get_absolute_url(self):
		return reverse('insurance:schaden-detail', args=(self.schadensmeldung.id,))

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(SchadensmeldungFile, self).save()