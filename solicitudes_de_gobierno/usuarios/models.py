from django.db import models
import datetime

# Create your models here.
class TipoDeUsuario(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipos_de_usuario"

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    segundo_nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=False)
    segundo_apellido = models.CharField(max_length=50, null=False)
    fecha_de_nacimiento = models.DateField(null=False)
    tipo_de_usuario = models.ForeignKey(
        TipoDeUsuario,
        on_delete=models.DO_NOTHING,
        null=False
    )
    # login_key = models.CharField()
    correo_electronico = models.CharField(max_length=100, null=False, default="missing_email")
    contrasena = models.CharField(null=False, default="missing_password")
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "usuarios"
