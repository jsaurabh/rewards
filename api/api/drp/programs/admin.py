from django.contrib import admin

from drp.programs import models


admin.site.register(models.Business)

admin.site.register(models.Campaign)

admin.site.register(models.Currency)
