from django.db import models
from django.urls import reverse, reverse_lazy


class Customer(models.Model):
	"""
	Django Model used to represent customers
	"""

	kundennummer = models.IntegerField(unique=True, primary_key=True)
	nachname = models.CharField(max_length=30)

	class Meta:
		"""
		Sets verbose names of customers to Kunde/Kunden
		"""
		verbose_name = "Kunde"
		verbose_name_plural = "Kunden"

	def __str__(self):
		return f'Kd{self.kundennummer}: {self.nachname}'

	def get_absolute_url(self):
		return reverse('customers:customer-detail', args=[str(self.kundennummer)])


# FIXME: We should not be able to set insurance without simultaneously creating an insurance policy object from our insurance app
class Bike(models.Model):
	"""
	Django Model used to represent bikes belonging to customers
	"""

	INSURANCE_OPTIONS = (
		('no', 'None'),
		('as', 'Assona'),
		('bl', 'Bikeleasing Service'),
		('bu', 'Businessbike'),
		('en', 'ENRA'),
		('eu', 'Eurorad'),
	)	

	kunde = models.ForeignKey(Customer, on_delete=models.CASCADE)
	beschreibung = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30, unique=True)
	insurance = models.CharField(
		max_length = 2,
		choices = INSURANCE_OPTIONS,
		blank = False,
		default = 'no',)

	class Meta:
		verbose_name = "Fahrrad"
		verbose_name_plural = "Fahrräder"

	def __str__(self):
		return self.rahmennummer

	def get_absolute_url(self):
		return reverse_lazy('customers:customer-detail', kwargs={'pk':self.kunde.kundennummer})
