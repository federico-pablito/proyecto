from django.shortcuts import render, redirect, get_object_or_404
from tablamadre.models import Tanque, Consumo, Repostaje
from .forms import ConsumoForm, CargarTanqueForm, RepostajeForm
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

##Gaspar recorda que para el JsonResponse tenes que copiar el archivo que cree en /static/assets/js/tanque.js
##sino jamas se te van a actualizar los tanques, trata de mantenerlo fuera de la app Combustible
##otra cosa, en el models repostaje agregale la fecha porfavor, que me olvide en su momento y me da paja borrar la base de datos
##el ivan quiere aplicar filtros para los historiales de repostaje y consumos no se que tipo de filtros aplicaste si los podes copiar
##para poder filtrar por fecha de repostaje/consumo en el historial un exito sino lo veo yo despues, tambien quiere poder imprimirlo en pdf
##Trata de copiar tal como esta solamente acomodando en el lugar correspondiente, los ajax son sensibles
##Tirame la goma xddd


@permission_required('auth.view_user')
def tanque_detail(request):
    tanques = Tanque.objects.all()
    return render(request, 'tanque_detail.html', {'tanques': tanques})


@permission_required('auth.view_user')
def actualizar_tanques(request):
    tanques = Tanque.objects.all()
    data = [{'nombre': tanque.nombre, 'capacidad': tanque.capacidad, 'cantidad_combustible': tanque.cantidad_combustible} for tanque in tanques]
    return JsonResponse(data, safe=False)

@permission_required('auth.view_user')
def registrar_consumo(request):
    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            consumo = form.save(commit=False)  # Con esto evito que se guarde de momento
            tanque = consumo.tanque
            if consumo.consumo_litros > tanque.cantidad_combustible:
                # logica para evitar monos
                messages.error(request, 'No hay suficiente combustible en el tanque.')
            else:
                # Actualizar el combustible
                consumo.save()  # Guardar el objeto de Consumo
                tanque.cantidad_combustible -= consumo.consumo_litros
                tanque.save()
                return redirect('detalleTanque')  # Si sale bien todo redirijo y mono feliz
    else:
        form = ConsumoForm()
    return render(request, 'registrar_consumo.html', {'form': form})


@permission_required('auth.view_user')
def historial_cargas(request):
    cargas = Consumo.objects.all()
    return render(request, 'historial_cargas.html', {'cargas': cargas})

@permission_required('auth.view_user')
def registrar_repostaje(request):
    if request.method == 'POST':
        form = RepostajeForm(request.POST)
        if form.is_valid():
            repostaje = form.save(commit=False)
            tanque = repostaje.tanque

            # Mas logica anti-monos
            if tanque.cantidad_combustible + repostaje.cantidad_litros > tanque.capacidad:
                messages.error(request, 'El repostaje excede la capacidad del tanque.')
                return redirect('repostaje')  # Redirigir de nuevo al formulario de repostaje

            # Si el mono hizo bien el laburo se guarda
            repostaje.save()
            tanque.cantidad_combustible += repostaje.cantidad_litros
            tanque.save()

            messages.success(request, 'Repostaje registrado correctamente.')
            return redirect('detalleTanque')  # Redirigir a principal y mono feliz
    else:
        form = RepostajeForm()
    return render(request, 'registrar_repostaje.html', {'form': form})


@permission_required('auth.view_user')
def historial_repostajes(request):
    # Obtener todos los repostajes
    repostajes = Repostaje.objects.all()
    return render(request, 'historial_repostaje.html', {'repostajes': repostajes})
