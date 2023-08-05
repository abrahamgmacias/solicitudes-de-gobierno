import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from solicitudes.models import Usuario, TiposDeUsuario
from django.views.decorators.csrf import csrf_exempt

# missing encryption
@csrf_exempt
def registrarUsuario(request):
    if request.method == 'POST': 
        data = json.loads(request.body.decode())
        tipo_instance = TiposDeUsuario.objects.get(id=data['tipo_de_usuario'])

        try:
            Usuario.objects.create(
                nombre = data['nombre'],
                segundo_nombre = data['segundo_nombre'],
                apellido = data['apellido'],
                segundo_apellido = data['segundo_apellido'],
                fecha_de_nacimiento = data['fecha_de_nacimiento'],
                tipo_de_usuario = tipo_instance,
                correo_electronico = data['correo_electronico'],
                contrasena = data['contrasena']
            )

            return JsonResponse(status=200, data={
                "res": "User was registered successfully."
            })

        except:
            return JsonResponse(status=400, data={
                "res": "Unable to register user."
            })
        

# Aplica para contrasena también
# No funciona con el correo
@csrf_exempt
def cambiarDatosUsuario(request):
    if request.method == "PUT":
        data = json.loads(request.body.decode())

        try:
            user_instance = Usuario.objects.get(correo_electronico=data['correo_electronico'])
        except Usuario.DoesNotExist:
            return JsonResponse(status=404, data={
                    "res": "No se encontró un usuario con ese correo."
                })

        for key, value in data.items():
            setattr(user_instance, key, value)
        
        user_instance.save()

        return JsonResponse(status=200, data={
            "res": "Se han cambiado los datos del usuario correctamente."
        })
