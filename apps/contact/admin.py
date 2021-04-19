from django.contrib import admin

from apps.contact import models

admin.site.register(models.PhoneContact)
admin.site.register(models.OutgoingCall)