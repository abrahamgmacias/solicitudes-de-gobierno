import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from usuarios.views import validarExistenciaUsuario, getDataUsuario

def index(request):
    context = {}
    if request.user is not None:
        usuario = json.loads(request.session['usuario_data'])

        if usuario['tipo_de_usuario'] == 1:
            context['usuario'] = usuario
        
        if usuario['tipo_de_usuario'] == 2: 
            return render(request, 'index-servidor.html', {'usuario': usuario })

    return render(request, 'index.html', context=context)