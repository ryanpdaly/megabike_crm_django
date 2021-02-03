from django.db import models
from django.urls import reverse, reverse_lazy

class Customer(models.Model):
	kundennummer = models.IntegerField(unique=True, primary_key=True)
	nachname = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Customer"
		verbose_name_plural = "Customers"

	def __str__(self):
		return f'Kd{self.kundennummer}: {self.nachname}'

	def get_absolute_url(self):
		return reverse('customers:customer-detail', args=[str(self.kundennummer)])

class Bike(models.Model):
	kundennummer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	
	beschreibung = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	INSURANCE_OPTIONS = (
		('no', 'None'),
		('as', 'Assona'),
		('bl', 'Bikeleasing Service'),
		('bu', 'Businessbike'),
		('en', 'ENRA'),
		('eu', 'Eurorad'),
	)

	versicherungsunternehmen = models.CharField(
		max_length = 2,
		choices = INSURANCE_OPTIONS,
		blank = False,
		default = 'no',)

	class Meta:
		verbose_name = "Bike"
		verbose_name_plural = "Bikes"

	def __str__(self):
		return self.beschreibung

	def get_absolute_url(self):
		return reverse_lazy('customers:bike-detail', kwargs={'pk':self.kundennummer.kundennummer, 'rn':self.rahmennummer})
