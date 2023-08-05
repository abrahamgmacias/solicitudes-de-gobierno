from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sign-in', views.registrarUsuario, name='login'),
    path('profile/update', views.cambiarDatosUsuario, name='cambiar-datos')
    # path('login/'),
    # path('sign-in/success'),
    # path('sign-in/failure'),
    # path('logout'),
    # path('restore/'),
    # path('restore/success'),
    # path('restore/failure'),
]
