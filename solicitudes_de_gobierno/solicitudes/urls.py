from django.urls import path
from . import views

urlpatterns = [
    path("registrar", views.registrarSolicitud, name="registrar-solicitud"),
    path("actualizar/<int:solicitud_id>", views.actualizarSolicitud, name="actualizar-solicitud"),
    path("historial/<int:solicitud_id>", views.getHistorialDeSolicitud, name="historial-de-solicitud")
]