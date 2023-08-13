from django.urls import path
from . import views

urlpatterns = [
    # path("registrar", views.registrarSolicitud, name="registrar-solicitud"),
    # path("actualizar/<int:solicitud_id>", views.actualizarSolicitud, name="actualizar-solicitud"),
    # path("historial/<int:solicitud_id>", views.getHistorialDeSolicitud, name="historial-de-solicitud"),
    # path("eliminar/<int:solicitud_id>", views.eliminarSolicitud, name="eliminar-solicitud"),
    # path("<int:solicitud_id>", views.getDataSolicitud, name="get-solicitud"),
    path("mis-solicitudes", views.verMisSolicitudes, name="ver-solicitudes"),
    path("<int:solicitud_id>", views.manageSolicitudes, name="solicitudes"),
    path("<int:solicitud_id>/comentarios", views.manageComentarios, name="comentarios")
]