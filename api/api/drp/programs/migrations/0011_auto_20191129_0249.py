# Generated by Django 2.2.7 on 2019-11-29 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("programs", "0010_auto_20191113_1502"),
    ]

    operations = [
        migrations.RenameField(
            model_name="currency", old_name="plural_label", new_name="label",
        ),
        migrations.RemoveField(model_name="currency", name="singular_label",),
    ]
