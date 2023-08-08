from django.contrib import admin
from .models import Prioridad, Accion, Espacio, Solicitud, Comentario, Reporte, Estatus, HistorialDeSolicitud

# Register your models here.
admin.site.register(Solicitud)
admin.site.register(Comentario)
admin.site.register(Reporte)
admin.site.register(Estatus)
admin.site.register(HistorialDeSolicitud)
admin.site.register(Accion)
admin.site.register(Espacio)
admin.site.register(Prioridad)