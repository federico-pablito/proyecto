from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import TablaMadre, Internos, Services, UnidadesdeProduccion, Reparaciones, Logistica, PartesDiarios, Novedades, Choferes

# Create your views here.
def mostrartablamadre(permission_required, request):
    lista_tm, lista_nombres = listador(TablaMadre.objects.all())
    return render(request, 'archivomustratabla.html', {'lista_tm':lista_tm, 'lista_nombres': lista_nombres })
    
def listador(permission_required, datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    nombres = [campo.name for campo in TablaMadre._meta.fields]
    internos = [campo.name for campo in Internos._meta.fields]
    services = [campo.name for campo in Services._meta.fields]
    unidadesdeproduccion = [campo.name for campo in UnidadesdeProduccion._meta.fields]
    reparaciones = [campo.name for campo in Reparaciones._meta.fields]
    logistica = [campo.name for campo in Logistica._meta.fields]
    partesdiarions = [campo.name for campo in PartesDiarios._meta.fields]
    novedades = [campo.name for campo in Novedades._meta.fields]
    lista_nombres = []
    for nombre in nombres:
        if nombre == 'internos':
            lista_nombres.append(nombre)
            for item in internos:
                lista_nombres.append(item)
        elif nombre == 'services':
            lista_nombres.append(nombre)
            for item in services:
                lista_nombres.append(item)
        elif nombre == 'unidadesdeproduccion':
            lista_nombres.append(nombre)
            for item in unidadesdeproduccion:
                lista_nombres.append(item)
        elif nombre == 'reparaciones':
            lista_nombres.append(nombre)
            for item in reparaciones:
                lista_nombres.append(item)
        elif nombre == 'logistica':
            lista_nombres.append(nombre)
            for item in logistica:
                lista_nombres.append(item)
        elif nombre == 'partesdiarions':
            lista_nombres.append(nombre)
            for item in partesdiarions:
                lista_nombres.append(item)
        elif nombre == 'novedades':
            lista_nombres.append(nombre)
            for item in novedades:
                lista_nombres.append(item)
        else:
            lista_nombres.append(nombre)    
    return lista_datos, lista_nombres
    permission_required = 'unidadesproduccion.urls_mostrartablamadre'