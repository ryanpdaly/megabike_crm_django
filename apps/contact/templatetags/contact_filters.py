from django import template


register = template.Library()

@register.filter(name='print_last_name')
def print_last_name(mitarbeiter):
	return mitarbeiter.split()[-1]