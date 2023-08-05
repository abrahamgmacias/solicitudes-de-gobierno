from django.contrib import admin
from .models import TipoDeUsuario, Usuario

# Register your models here.
admin.site.register(TipoDeUsuario)
admin.site.register(Usuario)