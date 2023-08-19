from django.db import models
from usuarios.models import Usuario
from django.utils import timezone
import datetime

class Accion(models.Model):
    nombre = models.CharField(max_length=100, null=False, unique=True)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        verbose_name_plural = "acciones"

    def __str__(self):
        return self.nombre

class Espacio(models.Model):
    nombre = models.CharField(max_length=100, null=False, unique=True)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return self.nombre

class Prioridad(models.Model):
    nombre = models.CharField(max_length=100, null=False, unique=True)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        verbose_name_plural = "prioridades"

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    accion = models.ForeignKey(
        Accion,
        null=False,
        on_delete=models.DO_NOTHING
    )
    espacio = models.ForeignKey(
        Espacio,
        null=False,
        on_delete=models.DO_NOTHING
    )
    usuario = models.ForeignKey(
        Usuario,
        null=False,
        on_delete=models.CASCADE
    )
    informacion_adicional = models.CharField(max_length=500, null=False)
    direccion = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=50, null=False)
    municipio_ciudad = models.CharField(max_length=50, null=False)
    codigo_postal = models.IntegerField(null=False)
    prioridad = models.ForeignKey(
        Prioridad,
        null=False,
        on_delete=models.CASCADE
    )
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        verbose_name = "solicitud"
        verbose_name_plural = "solicitudes"

class Comentario(models.Model):
    solicitud = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    texto = models.CharField(max_length=500)
    activo = models.BooleanField(null=False, default=True)
    usuario = models.ForeignKey(
        Usuario,
        null=False,
        on_delete=models.CASCADE
    )
    fecha_de_creacion= models.DateTimeField(null=False, default=timezone.now)

class Reporte(models.Model):
    solicitud = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    activo = models.BooleanField(null=False, default=True)
    usuario = models.ForeignKey(
        Usuario,
        null=False,
        on_delete=models.CASCADE
    )
    fecha_de_creacion= models.DateTimeField(null=False, default=timezone.now)

class Estatus(models.Model):
    nombre = models.CharField(null=False, unique=True)
    descripcion = models.CharField(null=False, max_length=200, default="Missing descripcion")
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        verbose_name = "estatus"
        verbose_name_plural = "estatuses"

class HistorialDeSolicitud(models.Model):
    solicitud = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    estatus = models.ForeignKey(
        Estatus,
        null=False,
        on_delete=models.CASCADE
    )
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        verbose_name = "historial_de_solicitud"
        verbose_name_plural = "historial_de_solicitudes"