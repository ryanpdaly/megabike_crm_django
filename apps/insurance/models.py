from django.db import models

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
	rahmennummer = models.CharField(max_length=30)
	vertragsnummer = models.CharField(max_length=10)
	beginn = models.DateField()

	versicherungskarte = models.FileField(blank=True)

	def __str__(self):
		return 'Assona'

class BikeleasingInfo(models.Model):
	PAKET_OPTIONS = [('P', 'Premium'), ('P+', 'Premium Plus')]
	BANK_OPTIONS = [('A', 'ALS Leasing GmbH'), ('H', 'Hofmann Leasing GmbH'),
				('D', 'Digital Mobility Leasing GmbH')]

	rahmennummer = models.CharField(max_length=30)

	nutzer_id = models.CharField(max_length=20)
	paket = models.CharField(max_length=20, choices=PAKET_OPTIONS)
	inspektion = models.BooleanField()
	leasingbank = models.CharField(max_length=1, choices=BANK_OPTIONS)
	beginn = models.DateField()

	versicherungskarte = models.FileField(blank=True)

	def __str__(self):
		return f'Bikeleasing: {self.paket}'

class BusinessbikeInfo(models.Model):
	PAKET_OPTIONS = (
		('D','Durchsicht'),
		('I', 'Inspektion'),
		('F', 'Full Service'),
		('E', 'Instandhaltungs+ enthalten'),
		('N', 'Instandhaltungs+ nicht enthalten'),
	)

	rahmennummer = models.CharField(max_length=30)

	beginn = models.DateField()
	ende = models.DateField()
	policenummer = models.CharField(max_length=30)
	paket = models.CharField(max_length=30)
	verschleiss_guthaben = models.BooleanField(default=False)

	versicherungskarte = models.FileField(blank=True)

	def __str__(self):
		return f'Businessbike: {self.get_paket_display}'

class EnraInfo(models.Model):
	rahmennummer = models.CharField(max_length=30)

	beginn = models.DateField()
	policenummer = models.CharField(max_length=20)

	versicherungskarte = models.FileField(blank=True)

	def __str__(self):
		return 'ENRA'

class EuroradInfo(models.Model):
	rahmennummer = models.CharField(max_length=30)

	beginn = models.DateField()
	vertragsnummer = models.CharField(max_length=20)

	def __str__(self):
		return 'Eurorad'