# Generated by Django 2.2.7 on 2019-11-11 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("programs", "0009_campaign_points_expire_after"),
        ("orders", "0001_initial"),
        ("rewards", "0003_auto_20191110_1621"),
    ]

    operations = [
        migrations.CreateModel(
            name="Point",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("expires_at", models.DateTimeField()),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="programs.Currency",
                    ),
                ),
                (
                    "line_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.LineItem",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Redemption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("reward", models.CharField(max_length=20)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(name="Redeemable",),
        migrations.AddField(
            model_name="point",
            name="redemption",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="rewards.Redemption",
            ),
        ),
        migrations.AddField(
            model_name="point",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
