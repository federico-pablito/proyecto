from django.shortcuts import render
from tablamadre.models import UnidadesdeProduccion
# Create your views here.
def verunidadproduccion(request):
    meta_clase = UnidadesdeProduccion._meta
    nombres = [campo.name for campo in meta_clase.fields]
    tabla = UnidadesdeProduccion.objects.all()
    lista_unidadesp, lista_nombres = listador(tabla)
    return render(request, 'holaquease.html', {'tabla': tabla, 'nombres': nombres, 'lista_unidadesp': lista_unidadesp, 'lista_nombres': lista_nombres,})

def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = UnidadesdeProduccion._meta
    nombres = [campo.name for campo in meta_clase.fields]
    lista_nombres = nombres
    return lista_datos, lista_nombres