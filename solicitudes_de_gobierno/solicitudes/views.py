import json
from usuarios.models import Usuario
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accion, Solicitud, HistorialDeSolicitud, Estatus, Espacio, Prioridad

def registrarHistorialDeSolicitud(solicitud_id):
    estatus_iniciado = 1
    # estatus_instance = Estatus.objects.get(estatus_id=estatus_iniciado)

    return HistorialDeSolicitud.objects.create(
        estatus_id=estatus_iniciado,
        solicitud_id=solicitud_id,
    )


@csrf_exempt
def actualizarHistorialDeSolicitud(request):
    pass


# Create your views here.
# Incluir API 
@csrf_exempt
def registrarSolicitud(request):
    if request.method == 'POST': 
        data = json.loads(request.body.decode())

        # accion_instance = Accion.objects.get(id=data['accion_id'])
        # espacio_instance = Espacio.objects.get(id=data['espacio_id'])
        # usuario_instance = Usuario.objects.get(id=data['usuario_id'])
        # prioridad_instance = Prioridad.objects.get(id=data['prioridad_id'])

        try:
            solicitud = Solicitud.objects.create(
                accion_id=data['accion_id'],
                espacio_id=data['espacio_id'],
                usuario_id=data['usuario_id'],
                informacion_adicional=data['informacion_adicional'],
                direccion=data['direccion'],
                estado=data['estado'],
                municipio_ciudad=data['municipio_ciudad'],
                codigo_postal=data['codigo_postal'],
                prioridad_id=data['prioridad_id'],
            )
            solicitud.save()

            registrarHistorialDeSolicitud(solicitud.id)

        except:
            return JsonResponse(status=400, data={"res": "No se pudo registrar la solicitud correctamente."})
            
        return JsonResponse(status=200, data={"res": "Se registró la solicitud correctamente."})





