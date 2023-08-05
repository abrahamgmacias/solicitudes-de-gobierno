# Generated by Django 4.2.4 on 2023-08-05 05:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TipoDeUsuario",
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
                ("nombre", models.CharField(max_length=20)),
                ("activo", models.BooleanField(default=True)),
                (
                    "fecha_de_creacion",
                    models.DateField(default=datetime.date(2023, 8, 4)),
                ),
            ],
            options={
                "verbose_name": "tipos_de_usuario",
            },
        ),
        migrations.CreateModel(
            name="Usuario",
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
                ("nombre", models.CharField(max_length=50)),
                ("segundo_nombre", models.CharField(max_length=50, null=True)),
                ("apellido", models.CharField(max_length=50)),
                ("segundo_apellido", models.CharField(max_length=50)),
                ("fecha_de_nacimiento", models.DateField()),
                (
                    "correo_electronico",
                    models.CharField(default="missing_email", max_length=100),
                ),
                ("contrasena", models.CharField(default="missing_password")),
                ("activo", models.BooleanField(default=True)),
                (
                    "fecha_de_creacion",
                    models.DateField(default=datetime.date(2023, 8, 4)),
                ),
                (
                    "tipo_de_usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="usuarios.tipodeusuario",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "usuarios",
            },
        ),
    ]