from django.db import models

class TiposDeUsuario(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipos_de_usuario"

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    segundo_nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, null=False)
    segundo_apellido = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField(null=False)
    tipo_de_usuario = models.ForeignKey(
        TiposDeUsuario,
        on_delete=models.DO_NOTHING,
        null=False
    )
    # login_key = models.CharField()
    correo_electronico = models.CharField(max_length=100, null=False, default="missing_email")
    contrasena = models.CharField(null=False, default="missing_password")
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "usuarios"


class TipoDeSolicitud(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    activo = models.BooleanField(null=False, default=True)
    fecha_de_creacion = models.DateField(null=False)

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
    fecha_de_creacion = models.DateField(null=False)

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
    fecha_de_creacion= models.DateField(null=False),

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
    fecha_de_creacion= models.DateField(null=False)

class Estatus(models.Model):
    nombre = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=500, null=False),
    activo = models.BooleanField(null=False, default=True)
    fecha_de_registro = models.DateField(null=False)

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
    fecha_de_creacion = models.DateField(null=False)

    class Meta:
        verbose_name = "historial_de_solicitud"
        verbose_name_plural = "historial_de_solicitudes"