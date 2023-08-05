from django.urls import path
from . import views

urlpatterns = [
    path('registrar', views.registrarUsuario, name="registrar-usuario"),
    path('actualizar', views.actualizarUsuario, name="actualizar-usuario"),
    path('datos', views.getDataUsuario, name="datos-usuario"),
]