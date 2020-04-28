from django.conf import settings
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=50)
    is_published = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, blank=True)  # TODO: normalize this.
    url = models.URLField(blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to="programs/businesses/logos", blank=True)
    customers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="customer_of"
    )
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="employee_of"
    )

    def __str__(self):
        return self.name


class Currency(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="currencies"
    )
    label = models.CharField(max_length=20)

    def __str__(self):
        return self.label


class Campaign(models.Model):
    name = models.CharField(max_length=20)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="campaigns"
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    starts_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)
    points_expire_after = models.DurationField(null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.business)
