from django.db import models

class InsuranceCompanies(models.Model):
	COMPANIES = (
				('ASSONA', 'Assona'),
				('BIKELEASING SERVICE', 'BikeleasingService'),
				('BUSINESSBIKE', 'Businessbike'),
				('ENRA', 'ENRA'),
				('EURORAD', 'Eurorad'),
			)
	company_name = models.CharField(max_length=30, default='ASSONA', choices=COMPANIES)
	
	def __str__(self):
		return self.name

class AssonaInfo(models.Model):
	'''
	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)
	fahrzeug = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)
	'''
	vertragsnummer = models.CharField(max_length=10)
	beginn = models.DateField()

	def __str__(self):
		return self.name

class BikeleasingInfo(models.Model):
	PAKET = [('P', 'Premium'), ('P+', 'Premium Plus')]
	BANKS = [('ALS', 'ALS Leasing GmbH'), ('Hofmann', 'Hofmann Leasing GmbH'),
				('Digital Mobility', 'Digital Mobility Leasing GmbH')]

	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)
	fahrzeug = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	nutzer_id = models.CharField(max_length=20)
	paket = models.CharField(max_length=20, choices=PAKET)
	inspektion = models.BooleanField()
	leasingbank = models.CharField(max_length=20, choices=BANKS)
	beginn = models.DateField()

class BusinessbikeInfo(models.Model):
	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)
	fahrzeug = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	beginn = models.DateField()
	ende = models.DateField()
	policenummer = models.CharField(max_length=30)
	paket = models.CharField(max_length=30)

class EnraInfo(models.Model):
	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)
	fahrzeug = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	beginnn = models.DateField()
	policenummer = models.CharField(max_length=20)

class EuroradInfo(models.Model):
	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)
	fahrzeug = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	beginn = models.DateField()
	vertragsnummer = models.CharField(max_length=20)