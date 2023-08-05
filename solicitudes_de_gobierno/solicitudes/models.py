from django.db import models
from usuarios.models import Usuario
import datetime

class TipoDeSolicitud(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

    class Meta:
        verbose_name = "tipo_de_solicitud"
        verbose_name_plural = "tipos_de_solicitud"

class Solicitud(models.Model):
    tipo_solicitud = models.ForeignKey(
        TipoDeSolicitud, 
        null=True,
        on_delete=models.DO_NOTHING
    )
    usuario = models.ForeignKey(
        Usuario,
        null=False,
        on_delete=models.CASCADE
    )
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

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
    fecha_de_creacion= models.DateField(null=False, default=datetime.date.today()),

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
    fecha_de_creacion= models.DateField(null=False, default=datetime.date.today())

class Estatus(models.Model):
    nombre = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=500, null=False),
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

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
    fecha_de_creacion = models.DateField(null=False, default=datetime.date.today())

    class Meta:
        verbose_name = "historial_de_solicitud"
        verbose_name_plural = "historial_de_solicitudes"