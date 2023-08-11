import json
from django.shortcuts import render
from django.forms import model_to_dict
from .models import Usuario, TipoDeUsuario
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# missing encryption
@csrf_exempt
def registrarUsuario(request):
    if request.method == 'POST': 
        data = json.loads(request.body.decode())
        tipo_instance = TipoDeUsuario.objects.get(id=data['tipo_de_usuario'])

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
                "res": "El usuario fue registrado exitosamente."
            })

        except:
            return JsonResponse(status=400, data={
                "res": "El usuario no pudo ser registrado."
            })
        

# Aplica para contrasena también
# No funciona con el correo
@csrf_exempt
def actualizarUsuario(request):
    if request.method == "PUT":
        data = json.loads(request.body.decode())
        
        if data["correo_electronico"] is None:
            return JsonResponse({"res": "Se requiere del correo electronico."}, status=400)

        user_instance = Usuario.objects.filter(correo_electronico=data['correo_electronico'], activo=True)

        for key, value in data.items():
            if key not in ['activo']:
                if hasattr(Usuario, key):
                    user_instance.update(**{key: value})
        
        user_instance.first().save()

        return JsonResponse(status=200, data={
            "res": "Se han cambiado los datos del usuario correctamente."
        })


@csrf_exempt
def getDataUsuario(request):
    if request.method == "GET":
        data = json.loads(request.body.decode())

        user_instance = Usuario.objects.filter(correo_electronico=data['correo_electronico'], activo=True)
        if user_instance.exists():
            return JsonResponse(status=200, data=list(user_instance.values())[0], safe=False)
        else: 
            return JsonResponse(status=404, data={
                "res": "No se encontró un usuario con ese correo."
            })


@csrf_exempt
def eliminarUsuario(request):
    if request.method == 'DELETE':
        data = json.loads(request.body.decode())
        
        user_instance = Usuario.objects.get(correo_electronico=data['correo_electronico'])

        if user_instance.exists():
            user_instance.activo = False
            user_instance.save()

            return JsonResponse(status=200, data={
                        "res": "Se eliminó el usuario correctamente."
                    })
            
        else: 
            return JsonResponse(status=404, data={
                    "res": "No se encontró un usuario con ese correo."
                })

        