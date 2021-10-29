from django.contrib import admin

from apps.customers.models import Customer, Bike

# Register your models here.

class BikeInline(admin.TabularInline):
	"""
	Inline display of bikes belonging to customer
	"""

	model = Bike
	extra = 1

class CustomerAdmin(admin.ModelAdmin):
	"""
	Custom admin behavior for customer model
	"""

	list_display = ('kundennummer', 'nachname')
	inlines = [BikeInline]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bike)