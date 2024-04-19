from django.shortcuts import render, redirect, get_object_or_404
from tablamadre.models import Tanque, Consumo, Repostaje
from .filters import consumo_filter, repostaje_filter
from .forms import ConsumoForm, CargarTanqueForm, RepostajeForm
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.modelo_a_excel import model_to_excel

##Gaspar recorda que para el JsonResponse tenes que copiar el archivo que cree en /static/assets/js/tanque.js
##sino jamas se te van a actualizar los tanques, trata de mantenerlo fuera de la app Combustible
##otra cosa, en el models repostaje agregale la fecha porfavor, que me olvide en su momento y me da paja borrar la base de datos
##el ivan quiere aplicar filtros para los historiales de repostaje y consumos no se que tipo de filtros aplicaste si los podes copiar
##para poder filtrar por fecha de repostaje/consumo en el historial un exito sino lo veo yo despues, tambien quiere poder imprimirlo en pdf
##Trata de copiar tal como esta solamente acomodando en el lugar correspondiente, los ajax son sensibles
##Tirame la goma xddd


@login_required
def tanque_detail(request):
    if request.user.has_perm('tablamadre.puede_ver_tanques'):
        tanques = Tanque.objects.all()
        return render(request, 'tanque_detail.html', {'tanques': tanques})
    else:
        # Realizar acciones para usuarios sin permiso
        return HttpResponse("No tienes permiso para ver los tanques, haber estudiao.")


@login_required
def actualizar_tanques(request):
    tanques = Tanque.objects.all()
    data = [{'nombre': tanque.nombre, 'capacidad': tanque.capacidad, 'cantidad_combustible': tanque.cantidad_combustible} for tanque in tanques]
    return JsonResponse(data, safe=False)

@login_required
def registrar_consumo(request):
    if request.user.has_perm('tablamadre.puede_ver_consumo'):
        if request.method == 'POST':
            form = ConsumoForm(request.POST)
            if form.is_valid():
                consumo = form.save(commit=False)  # Con esto evito que se guarde de momento
                tanque = consumo.tanque
                if consumo.consumo_litros > tanque.cantidad_combustible:
                    # lógica para evitar monos
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
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def historial_cargas(request):
    if request.user.has_perm('tablamadre.puede_ver_consumo'):
        cargas = Consumo.objects.all()
        filtro = consumo_filter(request.GET, queryset=cargas)
        if filtro.is_valid():
            cargas = filtro.qs
        return render(request, 'historial_cargas.html', {'cargas': cargas, 'filtro': filtro})
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")

@login_required
def registrar_repostaje(request):
    if request.user.has_perm('tablamadre.puede_ver_repostaje'):
        if request.method == 'POST':

            form = RepostajeForm(request.POST)
            if form.is_valid():
                repostaje = form.save(commit=False)
                tanque = repostaje.tanque

                # Más lógica anti-monos
                if tanque.cantidad_combustible + repostaje.cantidad_litros > tanque.capacidad:
                    messages.error(request, 'El repostaje excede la capacidad del tanque.')
                    return redirect('repostaje')  # Redirigir de nuevo al formulario de repostaje

                # Si el mono hizo bien el trabajo se guarda
                repostaje.save()
                tanque.cantidad_combustible += repostaje.cantidad_litros
                tanque.save()

                messages.success(request, 'Repostaje registrado correctamente.')
                return redirect('detalleTanque')  # Redirigir a principal y mono feliz
        else:
            form = RepostajeForm()
            return render(request, 'registrar_repostaje.html', {'form': form})
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def historial_repostajes(request):
    if request.user.has_perm('tablamadre.puede_ver_repostaje'):
        # Obtener todos los repostajes
        repostajes = Repostaje.objects.all()
        filtro = repostaje_filter(request.GET, queryset=repostajes)
        if filtro.is_valid():
            repostajes = filtro.qs
        return render(request, 'historial_repostaje.html', {'repostajes': repostajes, 'filtro': filtro})
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_consumos(request):
    if request.user.has_perm('tablamadre.puede_ver_consumo'):
        queryset = Consumo.objects.all()

        # No need to manually specify column headers now
        excel_file = model_to_excel(Consumo, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="HistorialConsumosCombustible.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_repostajes(request):
    if request.user.has_perm('tablamadre.puede_ver_repostaje'):
        queryset = Repostaje.objects.all()

        # No need to manually specify column headers now
        excel_file = model_to_excel(Repostaje, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="HistorialRepostajesCombustible.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
