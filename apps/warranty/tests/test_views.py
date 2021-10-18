from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from apps.warranty import models
from apps.common.tests import TestViewBasics

#Using quasi-test-oriented method to clean up some of the code base after writing these tests

class TestTicketList(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:ticket-list'
		self.url_kwargs = {'abteilung':'all', 'filter':'all'}
		self.url_path = 'warranty/all/all/'
		self.template_path = 'warranty/ticket_list.html'

		baker.make(models.ReklaTicket, _quantity=15)

class TestTicketCreate(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:ticket-create'
		self.url_kwargs = {}
		self.url_path = 'warranty/create/'
		self.template_path = 'warranty/ticket_create.html'

	# Additional tests for: get(), post(), form_valid(), form_invalid()

class TestTicketDisplay(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:ticket-display'
		self.url_kwargs = {'pk':1}
		self.url_path = 'warranty/1/display/'
		self.template_path = 'warranty/ticket_display.html'

		baker.make(models.ReklaTicket, id=1)

	# Additional tests for: get_context_data()

class TestTicketUpdate(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:ticket-update'
		self.url_kwargs = {'pk':1}
		self.url_path = 'warranty/1/update/'
		self.template_path = 'warranty/ticket_update.html'

		baker.make(models.ReklaTicket, id=1)

class TestAddFile(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:file-add'
		self.url_kwargs = {'pk':1}
		self.url_path = 'warranty/1/addfile/'
		self.template_path = 'warranty/file_add.html'

		baker.make(models.ReklaTicket, id=1)

	# Additional tests for: get_context_data(), form_valid()

class TestStatusCreate(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:status-add'
		self.url_kwargs = {'pk':1}
		self.url_path = 'warranty/1/addstatus/'
		self.template_path = 'warranty/status_add.html'

		baker.make(models.ReklaTicket, id=1)

	# Addtional tests for: get_context_data(), form_valid()

class TestFileDisplay(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData():
		super().setUpTestData()

		self.url_name = 'warranty:file-display'
		self.url_kwargs = {'pk':1, 'sk':1,}
		self.url_path = 'warranty/1/displayfile/1/'
		self.template_path = 'warranty/'

