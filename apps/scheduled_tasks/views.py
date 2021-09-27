from django.shortcuts import render
from django.core.mail import send_mail

from megabike_crm import local_settings


# Create your views here.

def fällig_versicherungs_tickets():
	send_mail(
		'Test scheduled email',
		'This is a test scheduled email.',
		'megabikeCRM@gmail.com',
		INSURANCE_EMPLOYEES,
		fail_silently = False,
		)