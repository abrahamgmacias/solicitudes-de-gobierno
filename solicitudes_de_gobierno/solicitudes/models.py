from django.db import models

class TiposDeUsuario(models.Model):
    nombre = models.CharField(max_length=20)
    activo = models.BooleanField()
    fecha_de_registro = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipos de usuario"

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length=20)
    segundo_nombre = models.CharField()
    apellido = models.CharField()
    segundo_apellido = models.CharField()
    fecha_de_nacimiento = models.DateField()
    tipo_de_usuario = models.ForeignKey(
        TiposDeUsuario,
        on_delete=models.CASCADE
    )
    # login_key = models.CharField()
    activo = models.BooleanField()
    fecha_de_registro = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "usuarios"


