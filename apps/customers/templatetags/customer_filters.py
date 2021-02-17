from django import template

from .. import models
from ...warranty import models as warranty_models

register = template.Library()

@register.filter(name='count_bikes')
def count_bikes(kdnr):
	return models.Bike.objects.filter(kunde=kdnr).count()

@register.filter(name='count_insured')
def count_insured(kdnr):
	return models.Bike.objects.filter(kunde=kdnr).exclude(insurance='no').count()

@register.filter(name='count_open_tickets')
def count_open_tickets(kdnr):
	open_tickets = []
	tickets = warranty_models.ReklaTicket.objects.filter(kunde=kdnr)

	for ticket in tickets:
		current_status = warranty_models.ReklaStatusUpdate.objects.filter(rekla_ticket=ticket.id).order_by('-id')[0]

		if current_status != 'Erledigt':
			open_tickets.append(tickets)
	
	return len(open_tickets)