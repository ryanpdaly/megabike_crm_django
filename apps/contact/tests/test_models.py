from datetime import date

from django.test import TestCase

from model_bakery import baker

from apps.contact import models


class TestPhoneContact(TestCase):
	@classmethod
	def setUpTestData(cls):
		pass

	def test_model_str(self):
		date_today = date.today()

		contact = baker.make(models.PhoneContact, kundenname='TestCustomer')
		self.assertEqual(str(contact), f'{date_today}: TestCustomer')