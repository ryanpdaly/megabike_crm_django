from django.contrib import admin

from apps.insurance import models

admin.site.register(models.AssonaInfo)
admin.site.register(models.BikeleasingInfo)
admin.site.register(models.BusinessbikeInfo)
admin.site.register(models.EnraInfo)
admin.site.register(models.EuroradInfo)
admin.site.register(models.Schadensmeldung)
admin.site.register(models.SchadensmeldungStatus)
admin.site.register(models.SchadensmeldungFile)