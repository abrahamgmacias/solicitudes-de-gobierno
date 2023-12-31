from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password 

# Create your models here.
class TipoDeUsuario(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

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
    correo_electronico = models.CharField(max_length=100, null=False, default="missing_email", unique=True)
    municipio_ciudad = models.CharField(max_length=50, null=False, default="missing_municipio_ciudad")
    estado = models.CharField(max_length=50, null=False, default="missing_estado")
    contrasena = models.CharField(null=False, default="missing_password")
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)
    last_login = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "usuarios"

    def save(self, *args, **kwargs):
        if self.contrasena and not self.contrasena.startswith('pbkdf2_sha256$'):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def checarContrasena(self, raw_contrasena):
        #  Cuando implemente los hashers utiliza check_password(raw_contrasena, self.contrasena)
        return raw_contrasena == self.contrasena