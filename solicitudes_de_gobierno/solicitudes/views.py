import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TipoDeSolicitud, Solicitud, HistorialDeSolicitud, Estatus



@csrf_exempt
def registrarHistorialDeSolicitud(solicitud_id):
    estatus_iniciado = 1
    estatus_instance = Estatus.objects.get(estatus_id=estatus_iniciado)

    HistorialDeSolicitud.objects.create(
        estatus_id=estatus_instance,
        solicitud_id=solicitud_id,
    )

    return 


@csrf_exempt
def actualizarHistorialDeSolicitud(request):
    pass


# Create your views here.
# Incluir API 
@csrf_exempt
def registrarSolicitud(request):
    if request.method == 'POST': 
        data = json.loads(request.body.decode())
        accion_id = Estatus.objects.get(id=data['accion_id'])
        espacio_id = Estatus.objects.get(id=data['espacio_id'])
        usuario_id = Estatus.objects.get(id=data['usuario_id'])
        prioridad_id = Estatus.objects.get(id=data['prioridad_id'])

        solicitud = Solicitud.objects.create(
            accion_id=accion_id,
            espacio_id=espacio_id,
            usuario_id=usuario_id,
            informacion_adicional=data['informacion_adicional'],
            direccion=data['direccion'],
            estado=data['estado'],
            municipio_ciudad=['municipio_ciudad'],
            codigo_postal=['codigo_postal'],
            prioridad_id=prioridad_id,
        )
        solicitud.save()

        registrarHistorialDeSolicitud(request, solicitud.id)




