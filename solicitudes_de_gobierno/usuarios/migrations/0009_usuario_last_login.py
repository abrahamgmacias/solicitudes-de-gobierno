# Generated by Django 4.2.4 on 2023-08-21 23:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0008_alter_usuario_fecha_de_nacimiento"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="last_login",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
