from django.db import models

from drp.programs.models import Business


class Category(models.Model):
    name = models.CharField(max_length=20)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return "{} (category {})".format(self.name, self.id)


class Item(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    image = models.ImageField(upload_to="catalog/items", blank=True)

    def __str__(self):
        return "Item(id={}, name={!r})".format(self.id, self.name)
