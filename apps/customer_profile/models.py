from django.db import models

class CustomerProfile(models.Model):
	kundennummer = models.IntegerField()
	nachname = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Customer"
		verbose_name_plural = "Customers"

	def __str__(self):
		return self.name

class FahrzeugProfile(models.Model):
	kundennummer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
	beschreibung = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Fahrzeug"
		verbose_name_plural = "Fahrzeuge"

	def __str__(self):
		return self.name
