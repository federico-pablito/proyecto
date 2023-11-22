from django.shortcuts import render
from tablamadre.models import Reparaciones, Internos, TablaMadre
from .forms import reparaciones_form
from .filters import reparaciones_filter

# Create your views here.
def reparaciones_main(request):
    # EL FILTRO NO FUNCIONA, LO USO Y EXPLOTA
    if request.method == 'POST':
        form = reparaciones_form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = reparaciones_form()
    tabla = Reparaciones.objects.all()
    #filter = reparaciones_filter(request.GET, queryset=tabla)
    lista_reparaciones, lista_nombres = listador(tabla)
    #ARREGLAR EL FILTRO
    return render(request, 'reparaciones_main.html', {'form':form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})
def reparaciones_crear(request):
    tabla = Reparaciones.objects.all()
    if request.method == 'POST':
        form = reparaciones_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_reparacion = form.save()
            interno = new_reparacion.interno
            if new_reparacion.estadoreparacion == 'Pendiente':
                new_reparacion.estadoequipo = 'Inoperativo'
            else:
                new_reparacion.estadoequipo = 'Operativo'
            up = Internos.objects.get(id=interno.id).up
            new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         reparaciones=new_reparacion, observaciones=descripcion, dolardia=0)
            new_tabla_madre.save()
    else:
        form = reparaciones_form()
    lista_reparaciones, lista_nombres = listador(tabla)
    return render(request, 'reparaciones_crear.html', {'tabla': tabla, 'form':form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})
def reparaciones_editar(request, id=None):
    tabla = Reparaciones.objects.all()
    if id:
        instancia = Reparaciones.objects.get(pk=id)
    else:
        instancia = Reparaciones()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = reparaciones_form(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('reparaciones-main')  # Redirige a la página de mostrar alquileres
    else:
        form = reparaciones_form(instance=instancia)
        lista_reparaciones, lista_nombres = listador(tabla)
    return render(request, 'editar_reparaciones.html', {'tabla': tabla, 'form': form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})
def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = Reparaciones._meta
    nombres = [campo.name for campo in meta_clase.fields]
    nombres_dependencias = [campo.name for campo in Internos._meta.fields]
    lista_nombres = []
    for nombre in nombres:
        if nombre == 'interno':
            for item in nombres_dependencias:
                if item == 'up':
                    lista_nombres.append(item)
                else:
                    lista_nombres.append(item)
            lista_nombres.append('ubicacion')
        else:
            lista_nombres.append(nombre)
    return lista_datos, lista_nombres