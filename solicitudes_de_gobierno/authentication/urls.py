from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout")
]