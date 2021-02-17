from django.contrib import admin

from . import models

admin.site.register(models.ReklaTicket)
admin.site.register(models.ReklaStatusUpdate)
admin.site.register(models.ReklaFile)