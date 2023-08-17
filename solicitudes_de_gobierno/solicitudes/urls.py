from django.urls import path
from . import views

urlpatterns = [
    path("mis-solicitudes", views.misSolicitudesView, name="ver-solicitudes"),
    path("mis-solicitudes/registrar", views.registrarSolicitudView, name="registrar-solicitudes"),
    path("mis-solicitudes/<int:solicitud_id>", views.solicitudView, name="solicitud-id"),
    path("mis-solicitudes/<int:solicitud_id>/eliminar", views.eliminarSolicitudView, name="eliminar-solicitud"),
    path("<int:solicitud_id>/comentarios", views.manageComentarios, name="comentarios")
]