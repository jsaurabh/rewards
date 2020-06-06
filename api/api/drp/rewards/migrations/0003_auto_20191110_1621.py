# Generated by Django 2.2.7 on 2019-11-10 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("programs", "0008_currency_business"),
        ("catalog", "0004_item_image"),
        ("rewards", "0002_auto_20191107_1205"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accumulationrule",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.Category",
            ),
        ),
        migrations.AlterField(
            model_name="accumulationrule",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.Item",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="accumulationrule",
            unique_together={("campaign", "category"), ("campaign", "item")},
        ),
    ]