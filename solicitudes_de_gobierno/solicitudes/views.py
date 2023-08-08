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






