# Generated by Django 2.2.7 on 2019-12-01 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rewards", "0011_auto_20191113_1837"),
    ]

    operations = [
        migrations.AlterField(
            model_name="point",
            name="line_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.LineItem",
            ),
        ),
    ]
