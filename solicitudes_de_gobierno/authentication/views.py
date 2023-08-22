import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .auth_backends.custom_auth import CustomAuthenticate

# View que maneja el inicio de sesión
def loginView(request):
    # Checa correo y contraseña con un authenticate custom y redirige al dashboard
    if request.method == 'POST':
        correo_electronico = request.POST.get('correo_electronico')
        contrasena = request.POST.get('contrasena')
        auth_backend = CustomAuthenticate()

        usuario = auth_backend.authenticate(request, correo_electronico=correo_electronico, contrasena=contrasena)

        if usuario is not None:
            login(request, usuario)

            usuario_data = {
                'correo_electronico': usuario.correo_electronico,
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'tipo_de_usuario': usuario.tipo_de_usuario.id
            }
            request.session['usuario_data'] = json.dumps(usuario_data)

            return redirect('landing-page')

        else:
            return render(request, 'login.html', {'res': "El correo o la contraseña son incorrectos."})

    if request.method == 'GET':
        return render (request, 'login.html')

