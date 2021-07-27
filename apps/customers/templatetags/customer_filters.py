from django import template

from apps.customers import models
from apps.insurance import models as insurance_models
from apps.warranty import models as warranty_models

register = template.Library()

@register.filter(name='count_bikes')
def count_bikes(kdnr):
	return models.Bike.objects.filter(kunde=kdnr).count()

@register.filter(name='count_insured')
def count_insured(kdnr):
	return models.Bike.objects.filter(kunde=kdnr).exclude(insurance='no').count()

@register.filter(name='count_open_tickets_all')
def count_open_tickets(kdnr):
	open_tickets = 0
	
	# Reworkable?, these loops are repetitive

	warranty_tickets = warranty_models.ReklaTicket.objects.filter(kunde=kdnr)

	for ticket in warranty_tickets:
		current_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket.id).order_by('-id')[0].status

		if current_status != 'erledigt':
			open_tickets += 1

	insurance_tickets = insurance_models.Schadensmeldung.objects.filter(kunde=kdnr)
	erledigt = ['be', 'ab']

	for ticket in insurance_tickets:
		current_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=ticket.id).order_by('-id')[0].status

		if current_status not in erledigt:
			open_tickets += 1

	return open_tickets

@register.filter(name='count_open_tickets_warranty')
def count_open_tickets(kdnr):
	open = 0
	
	tickets = warranty_models.ReklaTicket.objects.filter(kunde=kdnr)
	for ticket in tickets:
		current_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket.id).order_by('-id')[0].status

		if current_status != 'erledigt':
			open += 1
	
	return open