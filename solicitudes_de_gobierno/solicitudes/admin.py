from django.contrib import admin
from .models import TiposDeUsuario, Usuarios

# Register your models here.
admin.site.register(TiposDeUsuario)
admin.site.register(Usuarios)