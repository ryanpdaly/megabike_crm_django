from django.db import models

class CustomerProfile(models.Model):
	kundenummer = models.IntegerField()
	nachname = models.CharField(max_length=30)

class FahrzeugProfile(models.Model):
	beschreibung = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)
