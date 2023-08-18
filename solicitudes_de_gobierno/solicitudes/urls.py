from django.urls import path
from . import views

urlpatterns = [
    path('solicitudes-locales/', views.recientesSolicitudesLocalesView, name='solicitudes-locales'),
    path("mis-solicitudes/", views.misSolicitudesView, name="ver-solicitudes"),
    
    path("mis-solicitudes/<int:solicitud_id>/", views.gestionarSolicitud, name="gestionar-solicitudes"),
    
    path("mis-solicitudes/<int:solicitud_id>/eliminar", views.eliminarSolicitudView, name="eliminar-solicitud"),
    path("<int:solicitud_id>/comentarios/<int:comentario_id>", views.gestionarComentarios, name="gestionar-comentarios"),
    path("<int:solicitud_id>/comentarios", views.gestionarComentarios, name="gestionar-comentarios"),
]