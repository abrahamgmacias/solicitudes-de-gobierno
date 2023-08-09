import json
from usuarios.models import Usuario
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Accion, Solicitud, HistorialDeSolicitud, Estatus, Espacio, Prioridad

def registrarHistorialDeSolicitud(solicitud_id, estatus_id):
    historial_instance = HistorialDeSolicitud.objects.filter(estatus_id=estatus_id, solicitud_id=solicitud_id, activo=True)

    if historial_instance.exists():
        return

    return HistorialDeSolicitud.objects.create(
        estatus_id=estatus_id,
        solicitud_id=solicitud_id,
    )


@csrf_exempt
def actualizarSolicitud(request, solicitud_id):
    if request.method == "PUT":
        data = json.loads(request.body.decode())
        solicitud_instance = Solicitud.objects.filter(id=solicitud_id, activo=True)

        for key, value in data.items():
            if key not in ['activo']:
                if key == "estatus_id":
                    registrarHistorialDeSolicitud(solicitud_id, value)
                else: 
                    if hasattr(Solicitud, key):
                        solicitud_instance.update(**{key: value})
        
        solicitud_instance.first().save()

        return JsonResponse(status=200, data={
            "res": "La solicitud se ha actualizado correctamente."
        })


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

            estatus_iniciado = 1
            registrarHistorialDeSolicitud(solicitud.id, estatus_iniciado)

        except:
            return JsonResponse(status=400, data={"res": "No se pudo registrar la solicitud correctamente."})
            
        return JsonResponse(status=200, data={"res": "Se registró la solicitud correctamente."})


@csrf_exempt
def getHistorialDeSolicitud(request, solicitud_id):
    if request.method == "GET":
        historial_de_solicitudes = HistorialDeSolicitud.objects.select_related('estatus').filter(solicitud_id=solicitud_id, activo=True)
        historial_data = list(
            historial_de_solicitudes.values(
                "id", "solicitud_id", "estatus", "activo", "fecha_de_creacion"
            )
        )

        for hist, hist_data in zip(historial_de_solicitudes, historial_data):
            hist_data["estatus"] = hist.estatus.nombre

        return JsonResponse(status=200, data={"historial": historial_data})


@csrf_exempt
def getDataSolicitud(request, solicitud_id):
    if request.method == "GET":
        user_instance = Solicitud.objects.select_related('accion', 'espacio', 'prioridad').filter(id=solicitud_id, activo=True)
        user_data = list(user_instance.values(
            'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 'accion', 'espacio', 'prioridad', 'fecha_de_creacion' 
        ))[0]

        if user_instance.exists():
            user_data["accion"] = user_instance[0].accion.nombre
            user_data["espacio"] = user_instance[0].espacio.nombre
            user_data["prioridad"] = user_instance[0].prioridad.nombre

            return JsonResponse(status=200, data=user_data, safe=False)

        else: 
            return JsonResponse(status=404, data={
                "res": "No se encontró un a solicitud con ese ID."
            })


# Missing activo parameter
@csrf_exempt
def eliminarSolicitud(request, solicitud_id):
    if request.method == 'DELETE':
        solicitud_instance = Solicitud.objects.filter(id=solicitud_id, activo=True)

        if solicitud_instance.exists():
            solicitud = solicitud_instance.first()
            solicitud.activo = False
            solicitud.save()

            return JsonResponse(status=200, data={
                        "res": "Se eliminó la solicitud correctamente."
                    })
            
        else: 
            return JsonResponse(status=404, data={
                    "res": "No se encontró un usuario con ese correo."
                })