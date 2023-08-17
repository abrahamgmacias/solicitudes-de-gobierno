from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuarios.views import validarExistenciaUsuario, getDataUsuario

def index(request):
    sample_usuario = 1
    usuario = getDataUsuario(sample_usuario)

    return render(request, 'index.html', {'usuario': usuario['data']})