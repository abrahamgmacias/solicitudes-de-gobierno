# Generated by Django 4.2.4 on 2023-08-21 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0009_usuario_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="last_login",
            field=models.DateTimeField(default=None),
        ),
    ]
