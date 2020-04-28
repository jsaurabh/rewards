from django.conf import settings
from django.db import models
from django.utils import timezone

from drp.catalog.models import Item
from drp.programs.models import Business


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders_made"
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )


class LineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="line_items"
    )
    menu_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{} * Item(id={})".format(self.quantity, self.menu_item_id)
