import json
from .forms import SolicitudForm
from usuarios.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from usuarios.views import validarExistenciaUsuario
from django.views.decorators.csrf import csrf_exempt
from .models import Solicitud, HistorialDeSolicitud, Comentario

def misSolicitudesView(request):
    # Query user solicitudes
    sample_user_id = 1
    solicitudes = getSolicitudesDeUsuario(sample_user_id)

    if solicitudes['data'] != None:
        for solicitud in solicitudes['data']:
            solicitud['titulo'] = formatTituloSolicitud(solicitud)
    
    return render(request, 'solicitudes.html', {'res': solicitudes['res'], 'solicitudes': solicitudes['data']})


def solicitudView(request, solicitud_id):
    if request.method == 'GET':
        solicitud = getDataSolicitud(solicitud_id)

        if solicitud['data'] != None:
            solicitud_historial = getHistorialDeSolicitud(solicitud_id)
            comentarios = getComentarios(solicitud_id)

            package_steps = [
                "Registro",
                "Revisión",
                "Retroalimentación",
                "Completado",
            ]

            current_step = "Revisión"
            current_step_index = package_steps.index(current_step)
            previous_steps = package_steps[:current_step_index]

            return render(request, 'solicitud-individual.html', {
                'solicitud_data': solicitud['data'], 
                'solicitud_historial': solicitud_historial['data'],
                'package_steps': package_steps,
                'current_step': current_step,
                'previous_steps': previous_steps,
                'comentarios': comentarios
                }
            )
        
        else: 
            return render(request, 'missing-solicitud-individual.html',)


def editarSolicitudView(request, solicitud_id):
    return render(request, 'base/index.html')


def eliminarSolicitudView(request, solicitud_id):
    if request.method == 'DELETE':  
        solicitud = validarExistenciaSolicitud(solicitud_id)

        if solicitud['exists']:
            solicitud_instance = solicitud['solicitud'].first()
            solicitud_instance.activo = False
            solicitud_instance.save()

            return JsonResponse(status=200, data={"res": "Se eliminó la solicitud correctamente."})
                
        else: 
            return JsonResponse(status=404, data={"res": solicitud['data']})


def registrarSolicitudView(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        form.usuario = 1

        if form.is_valid():
            form.save() 

        return JsonResponse(status=200, data={'res': 'Se registró exitosamente la solicitud.'})

    if request.method == 'GET':
        form = SolicitudForm()

    return render(request, 'registrar-solicitud.html', {'form': form})


def manageSolicitudes(request, solicitud_id):
    try:
        data = json.loads(request.body.decode())
    except:
        pass

    if request.method == "GET":
        response = getDataSolicitud(solicitud_id)

    # if request.method == "POST":
    #     response = registrarSolicitud(data)

    if request.method == "PUT":
        response = actualizarSolicitud(data, solicitud_id)
    
    if request.method == "DELETE":
        response = eliminarSolicitud(solicitud_id)

    return response


# Add sort
def getSolicitudesDeUsuario(usuario_id):
    usuario = validarExistenciaUsuario(usuario_id)

    if usuario['exists']:
        solicitud_instances = Solicitud.objects.select_related('accion', 'espacio', 'prioridad').filter(usuario_id=usuario_id, activo=True)

        if solicitud_instances.exists():
            solicitudes_data = list(solicitud_instances.values(
                'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 'accion', 'espacio', 'prioridad', 'fecha_de_creacion'
            ))

            for solicitud_instance, solicitud_data in zip(solicitud_instances, solicitudes_data):
                solicitud_data["accion"] = solicitud_instance.accion.nombre
                solicitud_data["espacio"] = solicitud_instance.espacio.nombre
                solicitud_data["prioridad"] = solicitud_instance.prioridad.nombre

            return {'res': f'Tienes {len(solicitudes_data)} solicitudes activas.', 'data': solicitudes_data}

        else:
            return {'res': 'No tienes solicitudes activas', 'data': None}

    else:
       return {'res': usuario['res']}


def formatTituloSolicitud(solicitud_data):
    return f"ID: {solicitud_data['id']} - {solicitud_data['accion']} {solicitud_data['espacio']} - {solicitud_data['municipio_ciudad']}, {solicitud_data['estado']} - {solicitud_data['fecha_de_creacion']}"


def createNombreTicket(solicitud_data):
    pass


def validarExistenciaSolicitud(solicitud_id):
    solicitud_instance = Solicitud.objects.filter(id=solicitud_id, activo=True)

    if solicitud_instance.exists():
        return {'solicitud': solicitud_instance, 'exists': True}
    else:
        return {'solicitud': None, 'exists': False, 'res': "No existe solicitud activa con esa ID."}


def registrarHistorialDeSolicitud(solicitud_id, estatus_id):
    historial_instance = HistorialDeSolicitud.objects.filter(estatus_id=estatus_id, solicitud_id=solicitud_id, activo=True)

    if historial_instance.exists():
        return

    return HistorialDeSolicitud.objects.create(
        estatus_id=estatus_id,
        solicitud_id=solicitud_id,
    )


def actualizarSolicitud(data, solicitud_id):
    solicitud = validarExistenciaSolicitud(solicitud_id)

    if solicitud["exists"]:
        solicitud_instance = solicitud["solicitud"]

        for key, value in data.items():
            if key not in ['activo']:
                if key == "estatus_id":
                    registrarHistorialDeSolicitud(solicitud_id, value)
                else: 
                    if hasattr(Solicitud, key):
                        solicitud_instance.update(**{key: value})
            
        solicitud_instance.first().save()

        return JsonResponse(status=200, data={"res": "La solicitud se ha actualizado correctamente."})

    else:
        return JsonResponse(status=400, data={'res': solicitud['res']})


# Incluir API 
def registrarSolicitud(data):
    try:
        solicitud = Solicitud.objects.create(
            accion=data['accion'],
            espacio=data['espacio'],
            usuario=data['usuario'],
            informacion_adicional=data['informacion_adicional'],
            direccion=data['direccion'],
            estado=data['estado'],
            municipio_ciudad=data['municipio_ciudad'],
            codigo_postal=data['codigo_postal'],
            prioridad=data['prioridad'],
        )
        solicitud.save()

        estatus_iniciado = 1
        registrarHistorialDeSolicitud(solicitud.id, estatus_iniciado)

    except:
        return JsonResponse(status=400, data={"res": "No se pudo registrar la solicitud correctamente."})
            
    return JsonResponse(status=200, data={"res": "Se registró la solicitud correctamente."})


def getHistorialDeSolicitud(solicitud_id):
    historial_de_solicitudes = HistorialDeSolicitud.objects.select_related('estatus').filter(solicitud_id=solicitud_id, activo=True)
    historial_data = list(
        historial_de_solicitudes.values(
            "id", "solicitud_id", "estatus", "activo", "fecha_de_creacion"
            )
    )

    for hist, hist_data in zip(historial_de_solicitudes, historial_data):
        hist_data["estatus"] = hist.estatus.nombre

    return {"data": historial_data, 'res': 'Se obtuvo el historial con éxito.'}


def getDataSolicitud(solicitud_id):
    solicitud = validarExistenciaSolicitud(solicitud_id)

    if solicitud['exists']:
        solicitud_instance = solicitud['solicitud'].select_related('accion', 'espacio', 'prioridad')
        solicitud_data = list(solicitud_instance.values(
            'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 'accion', 'espacio', 'prioridad', 'fecha_de_creacion' 
        ))[0]

        solicitud_data["accion"] = solicitud_instance[0].accion.nombre
        solicitud_data["espacio"] = solicitud_instance[0].espacio.nombre
        solicitud_data["prioridad"] = solicitud_instance[0].prioridad.nombre

        return {'data': solicitud_data, 'res': 'Se obtuvó la información de manera exitosa.'}

    else:
        return {'data': None, 'res': 'No se encontró una solicitud con esa ID.'}





def getComentarios(solicitud_id):
    comentarios_instance = Comentario.objects.filter(activo=True, solicitud_id=solicitud_id)

    if comentarios_instance.exists():
        comentarios = list(comentarios_instance.values())
        return {'data': comentarios, 'res': 'Se obtuvó la información de manera exitosa.'}

    else:
        return {'data': None, 'res': 'Actualmente no hay comentarios.'}


def agregarComentario(data, solicitud_id):
    solicitud_instance = validarExistenciaSolicitud(solicitud_id)

    if solicitud_instance["exists"]:
        try:
            comentario = Comentario.objects.create(
                solicitud_id=solicitud_id,
                texto=data["texto"],
                usuario_id=data["usuario_id"]
            )
            comentario.save()

            return JsonResponse(data={"res": 'Se registró el comentario exitosamente.'}, status=200,)

        except: 
            return JsonResponse(data={"res": "No se pudo registrar el comentario. Intente de nuevo."}, status=400)

    else: 
        return JsonResponse(data={'res': solicitud_instance["res"]}, status=400)


def validarExistenciaComentario(comentario_id):
    comentario_instance = Comentario.objects.filter(id=comentario_id, activo=True)

    if comentario_instance.exists():
        return {'comentario': comentario_instance, 'exists': True}
    else:
        return {'comentario': None, 'exists': False, 'res': "No existe solicitud activa con esa ID."}


def eliminarComentario(comentario_id):
    comentario = validarExistenciaComentario(comentario_id)

    if comentario["exists"]:
        try:
            comentario_instance = comentario["comentario"].first()
            comentario_instance.activo = False
            comentario_instance.save()
            
            return JsonResponse(data={'res': 'El comentario fue eliminado con exito.'}, status=200)

        except:
            return JsonResponse(data={'res': 'El comentario no pudo ser eliminado.'}, status=400)

    return JsonResponse(data={'res': comentario["res"]}, status=400)


def actualizarComentario(data, comentario_id):
    comentario = validarExistenciaComentario(comentario_id)

    if comentario["exists"]:
        try:
            comentario_instance = comentario["comentario"].first()
            comentario_instance.texto = data["texto"]
            comentario_instance.save()
            
            return JsonResponse(data={'res': 'El comentario fue actualizado con exito.'}, status=200)

        except:
            return JsonResponse(data={'res': 'El comentario no pudo ser actualizado.'}, status=400)

    return JsonResponse(data={'res': comentario["res"]}, status=400)


@csrf_exempt
def manageComentarios(request, solicitud_id):
    try:
        data = json.loads(request.body.decode())
    except:
        pass

    if request.method == "POST":
        response = agregarComentario(data, solicitud_id)

    if request.method == "DELETE":
        comentario_id = request.GET.get('id')
        response = eliminarComentario(comentario_id)

    if request.method == "PUT":
        comentario_id = request.GET.get('id')
        response = actualizarComentario(data, comentario_id)

    return response