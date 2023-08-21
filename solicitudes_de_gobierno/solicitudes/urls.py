from django.urls import path
from . import views

urlpatterns = [
    path('explorar/', views.explorarSolicitudesView, name='explorar-solicitudes'),
    path('<int:solicitud_id>/', views.gestionarSolicitud, name='explorar-solicitud'),


    path("mis-solicitudes/", views.misSolicitudesView, name="ver-solicitudes"),
    path("mis-solicitudes/<int:solicitud_id>/", views.gestionarSolicitud, name="gestionar-solicitudes"),
    path("mis-solicitudes/registrar", views.registrarSolicitudView, name="registrar-solicitud"),
    path("mis-solicitudes/<int:solicitud_id>/eliminar", views.eliminarSolicitudView, name="eliminar-solicitud"),
    path("<int:solicitud_id>/comentarios/<int:comentario_id>", views.gestionarComentarios, name="gestionar-comentarios"),
    path("<int:solicitud_id>/comentarios", views.gestionarComentarios, name="gestionar-comentarios")
]