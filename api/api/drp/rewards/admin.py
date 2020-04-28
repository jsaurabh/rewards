from django.contrib import admin

from drp.rewards import models


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("currency", "user", "created_at", "expires_at", "was_redeemed")
    list_filter = ("currency", "user")

    def was_redeemed(self, obj):
        return obj.redemption is not None


admin.site.register(models.Redemption)
