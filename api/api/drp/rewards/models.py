from django.conf import settings
from django.db import models
from django.utils import timezone

from drp.catalog.models import Category, Item
from drp.programs.models import Campaign, Currency
from drp.orders.models import LineItem


class AccumulationRule(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="accumulation_rules"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (("campaign", "category", "item"),)

    def __str__(self):
        return "+{} for {} in {}".format(
            self.value, self.item if self.item else self.category, self.campaign,
        )


class RedemptionRule(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="redemption_rules"
    )
    reward = models.CharField(max_length=20)
    image = models.ImageField(upload_to="rewards", blank=True)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return "-{} for {} in {}".format(self.value, self.reward, self.campaign)


class PointQuerySet(models.QuerySet):
    def _unexpired(self):
        return self.exclude(expires_at__lt=timezone.now())

    def _unredeemed(self):
        return self.filter(redemption__isnull=True)

    def redeemable(self, *, currency, customer):
        return self._unexpired()._unredeemed().filter(currency=currency, user=customer)


class Point(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True)
    redemption = models.ForeignKey(
        "Redemption", on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    objects = PointQuerySet.as_manager()

    def __str__(self):
        return "1 {}".format(self.currency)


class Redemption(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    value = models.SmallIntegerField()
    reward = models.CharField(max_length=20)

    def __str__(self):
        return "{!r} redeemed {!r}".format(self.user, self.reward)
