# Generated by Django 4.2.4 on 2023-08-05 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("solicitudes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estatus",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
        migrations.AlterField(
            model_name="historialdesolicitud",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
        migrations.AlterField(
            model_name="reporte",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
        migrations.AlterField(
            model_name="solicitud",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
        migrations.AlterField(
            model_name="tipodesolicitud",
            name="fecha_de_creacion",
            field=models.DateField(default=datetime.date(2023, 8, 5)),
        ),
    ]