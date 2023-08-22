import json
from django.shortcuts import render

# Landing page view
def index(request):
    context = {}

    # Revisa si el usuario está logged in y muestra el tablero correspondiente para su tipo
    try: 
        usuario = json.loads(request.session['usuario_data'])

        if usuario['tipo_de_usuario'] == 1:
            context['usuario'] = usuario
        
        if usuario['tipo_de_usuario'] == 2: 
            return render(request, 'index-servidor.html', {'usuario': usuario })
        
    # Tablero genérico
    except:
        return render(request, 'index.html', context=context)