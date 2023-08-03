from django.db import models

class TiposDeUsuario(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    activo = models.BooleanField(null=False)
    fecha_de_registro = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipos de usuario"

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    segundo_nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, null=False)
    segundo_apellido = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField(null=False)
    tipo_de_usuario = models.ForeignKey(
        TiposDeUsuario,
        on_delete=models.CASCADE,
        null=False
    )
    # login_key = models.CharField()
    activo = models.BooleanField(null=False)
    fecha_de_registro = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "usuarios"


