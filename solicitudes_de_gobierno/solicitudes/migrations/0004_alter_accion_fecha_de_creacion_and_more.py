# Generated by Django 4.2.4 on 2023-08-19 22:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("solicitudes", "0003_alter_accion_fecha_de_creacion_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accion",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="comentario",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="espacio",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="estatus",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="historialdesolicitud",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="prioridad",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="reporte",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
        migrations.AlterField(
            model_name="solicitud",
            name="fecha_de_creacion",
            field=models.DateTimeField(default=datetime.date(2023, 8, 19)),
        ),
    ]
