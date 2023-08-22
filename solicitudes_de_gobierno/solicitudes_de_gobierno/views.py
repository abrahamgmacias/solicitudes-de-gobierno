import json
from datetime import date
from django.core.cache import cache
from django.shortcuts import render

# Landing page view
def index(request):
    context = {}
    # Intentar conseguir la locación del cache
    try:
        context['cache_locacion'] = cache.get(f'location:{date.today()}')
    except:
        pass

    # Revisa si el usuario está logged in y muestra el tablero correspondiente para su tipo
    try: 
        usuario = json.loads(request.session['usuario_data'])
        context['usuario'] = usuario

        if usuario['tipo_de_usuario'] == 1:
            return render(request, 'index.html', context=context)
        
        if usuario['tipo_de_usuario'] == 2: 
            return render(request, 'index-servidor.html', context=context)
        
    # Tablero genérico
    except:
        return render(request, 'index.html', context=context)