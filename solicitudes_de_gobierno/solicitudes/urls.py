from django.urls import path
from . import views

urlpatterns = [
    path("registrar", views.registrarSolicitud, name="registrar-solicitud"),
    path("actualizar/<int:solicitud_id>", views.actualizarEstatusDeSolicitud, name="actualizar-solicitud")
]