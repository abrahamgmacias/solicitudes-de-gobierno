# Generated by Django 4.2.4 on 2023-08-05 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tipodeusuario",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="correo_electronico",
            field=models.CharField(
                default="missing_email", max_length=100, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
    ]