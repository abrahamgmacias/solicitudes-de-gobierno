import json
import traceback
from datetime import date
from .forms import SolicitudForm
from django.core.cache import cache
from usuarios.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from usuarios.views import validarExistenciaUsuario, getDataUsuario
from authentication.views import checkUsuarioLoggedIn
from .models import Solicitud, HistorialDeSolicitud, Comentario, Estatus


# View para revisar mis solicitudes como usuario
def misSolicitudesView(request):
    # Workaround para @login_required
    usuario = checkUsuarioLoggedIn(request)
    if usuario == None:
        return redirect('authentication:login')

    # Consulta solicitudes de usuario
    solicitudes = getSolicitudesDeUsuario(usuario['id'])    

    context = {}
    if solicitudes['data'] != None:
        for solicitud in solicitudes['data']:
            solicitud['titulo'] = formatTituloSolicitud(solicitud)

        context['solicitudes'] = solicitudes['data']
    
    try:
        context['usuario'] = json.loads(request.session['usuario_data'])
        return render(request, 'solicitudes.html', context=context)

    except:
        return render(request, 'solicitudes.html', {'res': solicitudes['res'], 'solicitudes': solicitudes['data']})


# View para visualizar la información de una solicitud
def solicitudView(request, solicitud_id, usuario=None):
    solicitud = getDataSolicitud(solicitud_id)

    # Recopilar datos de la solicitud si existe
    if solicitud['data'] != None:
        solicitud_historial = getHistorialDeSolicitud(solicitud_id)['data']
        historial_steps = getHistorialSteps()
        comentarios = getComentarios(solicitud_id, 1)

        current_step = solicitud_historial[-1]["step"]
        current_step_index = historial_steps.index(current_step)
        previous_steps = historial_steps[:current_step_index]

        context = {
            'solicitud_data': solicitud['data'],
            'solicitud_historial': solicitud_historial,
            'historial_steps': historial_steps,
            'current_step': current_step,
            'previous_steps': previous_steps,
            'comentarios': comentarios,
            }

        try:
            context['usuario'] = json.loads(request.session['usuario_data'])

        except:
            pass

    # No existe 
    else: 
        return render(request, 'missing-solicitud-individual.html')

    # Checar si el usuario inició sesión
    if usuario is not None:
        # Revisa que el usuario creador sea el mismo que el visualizador para activar template de edición
        if solicitud['data']['usuario_id'] != usuario['id']:
            return render(request, 'solicitud-individual-ajena.html', context=context)

        return render(request, 'solicitud-individual.html', context=context)

    # Cuando no ha iniciado sesión o no se requiere iniciar sesión
    else: 
        # No requiere sesión, pero está conectado
        try: 
            if context['usuario']['tipo_de_usuario'] == 2:
                estatuses = getEstatuses()
                context['estatus'] = estatuses['data']
 
            return render(request, 'solicitud-individual-ajena.html', context=context)

        except:
            return render(request, 'solicitud-individual-ajena.html', context=context)
    

def getEstatuses():
    estatuses = Estatus.objects.filter(activo=True)
    estatuses_data = list(estatuses.values('id', 'nombre'))

    return {'res': "Se encontraron los valores correspondientes", 'data': estatuses_data}


# View intermedia para ver, borrar o actualizar una soicitud individual
def gestionarSolicitud(request, solicitud_id=None):
    login_required = request.GET.get('login_required') == 'True'
    
    # Workaround para @login_required
    if login_required:
        usuario = checkUsuarioLoggedIn(request)
        if usuario == None:
            return redirect('authentication:login')

    try:
        data = json.loads(request.body.decode())
    except:
        pass

    if request.method == 'GET':
        if login_required == True:
            response = solicitudView(request, solicitud_id, usuario)

        else:
            response = solicitudView(request, solicitud_id)

    if request.method == 'DELETE':
        response = eliminarSolicitudView(solicitud_id)

    if request.method == 'PUT':
        response = actualizarSolicitud(data, solicitud_id)

    return response


# Actualiza una solicitud de manera dinámica
def actualizarSolicitud(data, solicitud_id):
    solicitud = validarExistenciaSolicitud(solicitud_id)

    if solicitud["exists"]:
        solicitud_instance = solicitud["solicitud"]

        for key, value in data.items():
            if key not in ['activo']:
                # Si se modifica el estatus, se debe registar un paso más en el historial
                if key == "estatus_id":
                    registrarHistorialDeSolicitud(solicitud_id, value)
                else: 
                    if hasattr(Solicitud, key):
                        solicitud_instance.update(**{key: value})
            
        solicitud_instance.first().save()

        return JsonResponse(status=200, data={"res": "La solicitud se ha actualizado correctamente."})

    else:
        return JsonResponse(status=400, data={'res': solicitud['res']})


def eliminarSolicitudView(solicitud_id):
    solicitud = validarExistenciaSolicitud(solicitud_id)

    if solicitud['exists']:
        solicitud_instance = solicitud['solicitud'].first()
        solicitud_instance.activo = False
        solicitud_instance.save()

        return JsonResponse(status=200, data={"res": "Se eliminó la solicitud correctamente."})
                
    else: 
        return JsonResponse(status=404, data={"res": solicitud['data']})


# View para registar solicitudes
def registrarSolicitudView(request):
    # Workaround para @login_required
    usuario = checkUsuarioLoggedIn(request)
    if usuario == None:
        return redirect('authentication:login')

    context = {}
    try:
        context['usuario'] = json.loads(request.session['usuario_data'])
    except: 
        pass

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        form.usuario = 1

        if form.is_valid():
            solicitud = form.save() 
            historial = registrarHistorialDeSolicitud(solicitud.id, 1)

        return JsonResponse(status=200, data={'res': 'Se registró exitosamente la solicitud.'})

    if request.method == 'GET':
        form = SolicitudForm()

    context['form'] = form

    return render(request, 'registrar-solicitud.html', context=context)


# View para visualizar las últimas solicitudes en tu zona
def explorarSolicitudesView(request):
    # Agarra cache de la localización
    locacion_cache = cache.get(f'location:{date.today()}')

    if locacion_cache != None:
        solicitudes = getSolicitudesPorParametros({
            'municipio_ciudad': locacion_cache['ciudad'],
            'activo': True
        })

        solicitudes_recientes = getSolicitudesRecientes()
        context = {
            'res': solicitudes['res']   
        }

        if solicitudes['data'] != None:
            for solicitud in solicitudes['data']:
                solicitud['titulo'] = formatTituloSolicitud(solicitud)

            context['solicitudes'] = solicitudes['data']

        if solicitudes_recientes['data'] != None:
            for solicitud in solicitudes_recientes['data']:
                solicitud['titulo'] = formatTituloSolicitud(solicitud)

            context['solicitudes_recientes'] = solicitudes_recientes['data']

        try: 
            context['usuario'] = json.loads(request.session['usuario_data'])
            return render(request, 'solicitudes-recientes.html', context=context )

        except: 
            return render(request, 'solicitudes-recientes.html', context=context )


def getSolicitudesRecientes():
    solicitudesRecientes = Solicitud.objects.select_related('accion', 'espacio', 'prioridad').order_by('-id')[:5]

    solicitudesRecientes_data = list(solicitudesRecientes.values(
                'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 
                'accion', 'espacio', 'prioridad', 'fecha_de_creacion'
            ))

    for solicitud_instance, solicitud_data in zip(solicitudesRecientes, solicitudesRecientes_data):
        solicitud_data["accion"] = solicitud_instance.accion.nombre
        solicitud_data["espacio"] = solicitud_instance.espacio.nombre
        solicitud_data["prioridad"] = solicitud_instance.prioridad.nombre

    return {"res": "Aquí están las cinco últimas solicitudes.", "data": solicitudesRecientes_data}


# Utilizada para guardar la localización en el cache
def cacheLocalizacion(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        # Check if the location data is in the cache based on user ID
        cache_key = f'location:{date.today()}'

        # Guarda la localización en el cache
        info_localizacion = {'estado': data['estado'], 'ciudad': data['ciudad']}

        # Lo guarda en el cache por una hora
        cache.set(cache_key, info_localizacion, timeout=3600)  

        return JsonResponse({'location': info_localizacion})

    else:
        return JsonResponse({'error': 'Solicitud invalida.'}, status=400)


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


# Consulta las solicitudes de manera dinámica
def getSolicitudesPorParametros(condiciones_de_filtro):
    solicitudes = Solicitud.objects.select_related('accion', 'espacio', 'prioridad').filter(**condiciones_de_filtro)

    if solicitudes.exists():
        solicitudes_data = list(solicitudes.values(
            'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 'accion', 'espacio', 'prioridad', 'fecha_de_creacion' 
        ))

        for solicitud_inst, solicitud_data in zip(solicitudes, solicitudes_data):
            solicitud_data["accion"] = solicitud_inst.accion.nombre
            solicitud_data["espacio"] = solicitud_inst.espacio.nombre
            solicitud_data["prioridad"] = solicitud_inst.prioridad.nombre

        return { 'res': f'Existen {len(solicitudes)} solicitudes activas cerca de ti.', 'data': solicitudes_data }

    else: 
        return { 'res': 'Actualmente no hay solicitudes activas cerca de ti.', 'data': None}


# Da formato legible a una solicitud
def formatTituloSolicitud(solicitud_data):
    return f"ID: {solicitud_data['id']} - {solicitud_data['accion']} {solicitud_data['espacio']} - {solicitud_data['municipio_ciudad']}, {solicitud_data['estado']} - {solicitud_data['fecha_de_creacion']}"


# Busca la solicitud en base a su ID y regresa el la solicitud
def validarExistenciaSolicitud(solicitud_id):
    solicitud_instance = Solicitud.objects.filter(id=solicitud_id, activo=True)

    if solicitud_instance.exists():
        return {'solicitud': solicitud_instance, 'exists': True}
    else:
        return {'solicitud': None, 'exists': False, 'res': "No existe solicitud activa con esa ID."}


# Agrega un nuevo paso en el historial para una solicitud
def registrarHistorialDeSolicitud(solicitud_id, estatus_id):
    historial_instance = HistorialDeSolicitud.objects.filter(estatus_id=estatus_id, solicitud_id=solicitud_id, activo=True)

    if historial_instance.exists():
        return JsonResponse(status=400, data={'res': 'No se actualizó el historial dado un nulo cambio en el estatusd de la solicitud.'})

    historial_entry = HistorialDeSolicitud.objects.create(
        estatus_id=estatus_id,
        solicitud_id=solicitud_id,
    )
    historial_entry.save()

    return JsonResponse(status=200, data={'res': 'Se actualizó el historial con éxito.'})


# Hardcoded lista de pasos de historial
def getHistorialSteps():
    return [
        "Registro",
        "En revisión",
        "Retroalimentación",
        "Completado",
    ]


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


# Recopila el historial de solicitud
def getHistorialDeSolicitud(solicitud_id):
    historial_de_solicitudes = HistorialDeSolicitud.objects.select_related('estatus').filter(solicitud_id=solicitud_id, activo=True)
    historial_data = list(
        historial_de_solicitudes.values(
            "id", "solicitud_id", "estatus", "activo", "fecha_de_creacion"
            )
    )

    # Actualiza el paso actual del historial de solicitud para el usuario
    for hist, hist_data in zip(historial_de_solicitudes, historial_data):
        estatus = hist_data['estatus']
        if estatus == 1:
            hist_data['step'] = "Registro"

        if estatus == 2:
            hist_data['step'] = "En revisión"

        if estatus in [3, 4, 5]:
            hist_data['step'] = "Retroalimentación"

        if estatus == 6:
            hist_data['step'] = "Completado"

        hist_data["estatus"] = hist.estatus.nombre
        hist_data['descripcion'] = hist.estatus.descripcion

    return {"data": historial_data, 'res': 'Se obtuvo el historial con éxito.'}


# Recopila todos los datos de la solicitud existente
def getDataSolicitud(solicitud_id):
    solicitud = validarExistenciaSolicitud(solicitud_id)

    if solicitud['exists']:
        solicitud_instance = solicitud['solicitud'].select_related('accion', 'espacio', 'prioridad', 'usuario')
        solicitud_data = list(solicitud_instance.values(
            'id', 'informacion_adicional', 'direccion', 'estado', 'municipio_ciudad', 'codigo_postal', 'accion', 'espacio', 'prioridad', 'fecha_de_creacion', 'usuario_id'
        ))[0]

        # Formatea titulos para más fácil lectura
        titulos = {
            'id', 'Información adicional', 'Dirección', 'Estado', 'Municipio o ciudad', 'Código postal', 'Fecha de creación', "Accion", "Espacio", "Prioridad",
        }

        # Actualizar el JSON de solicitud
        solicitud_data["accion"] = solicitud_instance[0].accion.nombre
        solicitud_data["espacio"] = solicitud_instance[0].espacio.nombre
        solicitud_data["prioridad"] = solicitud_instance[0].prioridad.nombre

        return {'data': solicitud_data, 'res': 'Se obtuvó la información de manera exitosa.', 'titulos': titulos}

    else:
        return {'data': None, 'res': 'No se encontró una solicitud con esa ID.', 'formatted_data': None}


# Consulta todos los comentarios de una solicitud
def getComentarios(solicitud_id, usuario_id):
    comentarios_instance = Comentario.objects.select_related('usuario').filter(activo=True, solicitud_id=solicitud_id)

    if comentarios_instance.exists():
        comentarios_data = list(comentarios_instance.values(
            'id', 'texto', 'fecha_de_creacion', 'solicitud_id', 'usuario', 'usuario_id'
        ))

        for comentario_instance, comentario_data in zip(comentarios_instance, comentarios_data):
            comentario_data["usuario"] = f'{comentario_instance.usuario.nombre} {comentario_instance.usuario.apellido}'
            
            # Checar si el comentario corresponde al usuario y dar privilegio de eliminar
            if comentario_data["usuario_id"] == usuario_id:
                comentario_data['removible'] = True

            else:
                comentario_data['removible'] = False

        return {'data': comentarios_data, 'res': 'Se obtuvó la información de manera exitosa.'}

    else:
        return {'data': None, 'res': 'Actualmente no hay comentarios. Sé el primero en escribir uno...'}


# Valida la existencia del comentario
def validarExistenciaComentario(comentario_id):
    comentario_instance = Comentario.objects.filter(id=comentario_id, activo=True)

    if comentario_instance.exists():
        return {'comentario': comentario_instance, 'exists': True}
    else:
        return {'comentario': None, 'exists': False, 'res': "No existe solicitud activa con esa ID."}


# Agrega un comentario a una solicitud
def agregarComentario(data, solicitud_id):
    solicitud_instance = validarExistenciaSolicitud(solicitud_id)

    if solicitud_instance["exists"]:
        comentario = Comentario.objects.create(
            solicitud_id=solicitud_id,
            texto=data["texto"],
            usuario_id=1
        )

        comentario.save()
                
        return JsonResponse(status=200, data={'res': 'El comentario se agregó con éxito.'})

    else:
        return JsonResponse(status=400, data={'res': 'No se encontró una solicitud activa con esa ID.'}) 


# Elimina el comentario de una solicitud tras validar su existencia
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


# Actualiza el comentario de una solicitud tras validar su existencia
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


# Función intermediaria para borrar y publicar un comentario en una solicitud
def gestionarComentarios(request, solicitud_id=None, comentario_id=None):
    try:
        data = json.loads(request.body.decode())
    except:
        pass

    if request.method == "POST":
        response = agregarComentario(data, solicitud_id)

    if request.method == "DELETE":
        response = eliminarComentario(comentario_id) 

    return response