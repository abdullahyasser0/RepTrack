# Generated by Django 4.2.16 on 2024-11-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(default="", max_length=8, unique=True)),
                ("name", models.CharField(default="", max_length=20)),
            ],
        ),
    ]
