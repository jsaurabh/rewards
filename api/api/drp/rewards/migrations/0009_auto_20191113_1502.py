# Generated by Django 2.2.7 on 2019-11-13 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rewards", "0008_accumulationrule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="point",
            name="redemption",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="rewards.Redemption",
            ),
        ),
    ]
