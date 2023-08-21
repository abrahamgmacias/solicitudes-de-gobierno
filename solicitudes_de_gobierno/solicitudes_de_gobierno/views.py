from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuarios.views import validarExistenciaUsuario, getDataUsuario

def index(request):
    sample_ciudadano = 1
    sample_servidor = 2

    usuario_instance = getDataUsuario(sample_servidor)
    usuario_data = usuario_instance['data']

    if usuario_data['tipo_de_usuario'] == "Ciudadano":
        return render(request, 'index.html', {'usuario': usuario_data})
    
    else: 
        return render(request, 'index-servidor.html', {'usuario': usuario_data})