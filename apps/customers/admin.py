from django.contrib import admin

from .models import Customer, Bike

# Register your models here.

class BikeInline(admin.TabularInline):
	model = Bike
	extra = 1

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('kundennummer', 'nachname')
	inlines = [BikeInline]

class BikeAdmin(admin.ModelAdmin):
	pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bike, BikeAdmin)