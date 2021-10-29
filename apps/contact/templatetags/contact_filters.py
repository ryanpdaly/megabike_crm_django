from django import template


register = template.Library()

@register.filter(name='print_last_name')
def print_last_name(mitarbeiter):
	"""
	A custom django template filter to show only the last word of a
	string. Used mostly to print the last name of an employee
	"""
	
	return mitarbeiter.split()[-1]