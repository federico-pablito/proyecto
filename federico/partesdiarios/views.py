from django.shortcuts import render, redirect
from tablamadre.models import PartesDiarios, Internos, Reparaciones, TablaMadre
from .forms import partediario_form

# Create your views here.
def partesdiario_main(request):
    partediario = PartesDiarios.objects.all()
    lista_partediario, lista_nombres = listador(partediario)
    # HACER EL FILTRO
    return render(request, 'partediario_main.html', {'lista_partediario': lista_partediario, 'lista_nombres': lista_nombres,})

def partediario_crear(request):
    if request.method == 'POST':
        form = partediario_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_logistica = form.save()
            interno = new_logistica.interno
            up = Internos.objects.get(id=interno.id).up
            last_reparacion = Reparaciones.objects.filter(interno=interno).last()
            if last_reparacion is None:
                last_reparacion = None
            new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         logistica=new_logistica, observaciones=descripcion, dolardia=0, reparaciones=last_reparacion)
            new_tabla_madre.save()
            return redirect('partesdiario_main')
    else:
        form = partediario_form()
    return render(request, 'partediario_crear.html', {'form': form})

def partediario_editar(request):
    if id:
        instancia = PartesDiarios.objects.get(pk=id)
    else:
        instancia = PartesDiarios()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = partediario_form(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('partesdiario_main')
    else:
        form = partediario_form(instance=instancia)
    return render(request, 'partediario_editar.html',
                  { 'form': form})
def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = PartesDiarios._meta
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