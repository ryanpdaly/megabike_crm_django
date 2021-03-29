from django.test import TestCase

from apps.customers import models

class TestCustomerModel(TestCase):
	@classmethod
	def setUpTestData(cls):
		models.Customer.objects.create(kundennummer=12345, nachname='TestCustomer',)

	def test_label_kundennummer(self):
		customer = models.Customer.objects.get(kundennummer=12345)
		field_label = customer._meta.get_field('kundennummer').verbose_name
		self.assertEqual(field_label, 'kundennummer')

	def test_label_nachname(self):
		customer = models.Customer.objects.get(kundennummer=12345)
		field_label = customer._meta.get_field('nachname').verbose_name
		self.assertEqual(field_label, 'nachname')

	def test_get_absolute_url(self):
		customer = models.Customer.objects.get(kundennummer = 12345)
		self.assertEqual(customer.get_absolute_url(), '/customers/kd12345/detail/')

	def test_model_str(self):
		customer = models.Customer.objects.get(kundennummer=12345)
		self.assertEqual(str(customer), 'Kd12345: TestCustomer')


class TestBikeModel(TestCase):
	@classmethod
	def setUpTestData(cls):
		models.Customer.objects.create(kundennummer='12345', nachname='TestCustomer')
		models.Bike.objects.create(kunde=models.Customer.objects.get(kundennummer=12345),
										beschreibung='TestBike', rahmennummer='TestRahmennummer',
										insurance='no')

	def test_label_rahmennummer(self):
		bike = models.Bike.objects.get(id=1)
		field_label = bike._meta.get_field('rahmennummer').verbose_name
		self.assertEqual(field_label, 'rahmennummer')

	def test_get_absolute_url(self):
		bike = models.Customer.objects.get(kundennummer=12345)
		self.assertEqual(bike.get_absolute_url(), '/customers/kd12345/detail/')

	def test_model_str(self):
		bike = models.Bike.objects.get(id=1)
		self.assertEqual(str(bike), 'TestRahmennummer')