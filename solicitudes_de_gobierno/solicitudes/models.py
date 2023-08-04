from django.db import models

class TiposDeUsuario(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    activo = models.BooleanField(null=False)
    fecha_de_creacion = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipos de usuario"

class Usuario(models.Model):
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
    fecha_de_creacion = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "usuarios"


class TipoDeSolicitud(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    activo = models.BooleanField(null=False)
    fecha_de_creacion = models.DateField(null=False)

    class Meta:
        verbose_name = "tipo_de_solicitud"
        verbose_name_plural = "tipos_de_solicitud"

class Solicitud(models.Model):
    tipo_solicitud_id = models.ForeignKey(
        TipoDeSolicitud, 
        null=True
    )
    usuario_id = models.ForeignKey(
        Usuario,
        null=False
    )
    activo = models.BooleanField(null=False)
    fecha_de_creacion = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "solicitudes"

class Comentario(models.Model):
    solicitud_id = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    texto = models.CharField(max_length=500)
    activo = models.BooleanField(null=False)
    usuario_id = models.ForeignKey(
        Usuario,
        null=False
    )
    fecha_de_creacion= models.DateField(null=False),

class Reporte(models.Model):
    solicitud_id = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    activo = models.BooleanField(null=False)
    usuario_id = models.ForeignKey(
        Usuario,
        null=False
    )
    fecha_de_creacion= models.DateField(null=False)

class Estatus(models.Model):
    nombre = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=500, null=False),
    activo = models.BooleanField(null=False)
    fecha_de_registro = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "Estatuses"

class HistorialDeSolicitud(models.Model):
    solicitud_id = models.ForeignKey(
        Solicitud,
        null=False,
        on_delete=models.CASCADE
    )
    estatus_id = models.ForeignKey(
        Estatus,
        null=False
    )
    activo = models.BooleanField(null=False)
    fecha_de_creacion = models.DateField(null=False)

    class Meta:
        verbose_name = "historial_de_solicitud"
        verbose_name_plural = "historial_de_solicitudes"