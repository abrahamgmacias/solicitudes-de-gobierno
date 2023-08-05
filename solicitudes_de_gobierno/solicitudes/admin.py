from django.contrib import admin
from .models import TipoDeSolicitud, Solicitud, Comentario, Reporte, Estatus, HistorialDeSolicitud

# Register your models here.
admin.site.register(TipoDeSolicitud)
admin.site.register(Solicitud)
admin.site.register(Comentario)
admin.site.register(Reporte)
admin.site.register(Estatus)
admin.site.register(HistorialDeSolicitud)