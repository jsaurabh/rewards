# Generated by Django 2.2.7 on 2019-11-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rewards", "0005_auto_20191111_0233"),
    ]

    operations = [
        migrations.AddField(
            model_name="redemptionrule",
            name="image",
            field=models.ImageField(blank=True, upload_to="rewards"),
        ),
    ]