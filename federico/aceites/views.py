from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tablamadre.admin import Permission
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from tablamadre.models import TanqueAceite, ConsumoAceite, RepostajeAceite
from .forms import ConsumoAceiteForm, RepostajeAceiteForm, TanqueAceite
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages


# Create your views here.
@login_required
def aceite_detail(request):
    if request.user.has_perm('tablamadre.puede_ver_aceites'):
        aceites = TanqueAceite.objects.all()
        return render(request, 'mostrar_tanques_aceite.html', {'aceite': aceites})
    else:
        # Realizar acciones para usuarios sin permiso
        return HttpResponse("No tienes permiso para ver los tanques, haber estudiao.")


def actualizar_aceites(request):
    if request.user.has_perm('tablamadre.puede_ver_aceites'):
        aceites = TanqueAceite.objects.all()
        data = [{'nombre': aceite.nombre,
                 'tipo de aceite': aceite.tipo_aceite,
                 'capacidad': aceite.capacidad_aceite,
                 'cantidad': aceite.cantidad_aceite} for aceite in aceites]
        return JsonResponse(data, safe=False)
    else:
        # Manejar el caso en que el usuario no tenga los permisos adecuados
        return JsonResponse({'error': 'No tienes permiso para ver los aceites.'})


def registrar_consumo_aceite(request):
    if request.user.has_perm('tablamadre.puede_ver_consumo'):
        if request.method == 'POST':
            form = ConsumoAceiteForm(request.POST)
            if form.is_valid():
                consumo = form.save(commit=False)
                tanqueac = consumo.tanque_aceite  # Obtener el tanque de aceite relacionado al consumo
                if consumo.cantidad_consumida > tanqueac.cantidad_aceite:  # Comparar los valores de cantidad_consumida y cantidad_aceite
                    messages.error(request, 'No hay suficiente aceite en el tanque.')
                else:
                    consumo.save()
                    tanqueac.cantidad_aceite -= consumo.cantidad_consumida
                    tanqueac.save()
                    return redirect('detalleAceite')
        else:
            form = ConsumoAceiteForm()
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return render(request, 'registrar_consumo_aceite.html', {'form': form})


def historial_consumos_aceite(request):
    cargas = ConsumoAceite.objects.all()
    return render(request, 'historial_consumo_aceite.html', {'cargas': cargas})


def registrar_repostaje_aceite(request):
    if request.user.has_perm('tablamadre.puede_ver_repostaje'):
        if request.method == 'POST':
            form = RepostajeAceiteForm(request.POST)
            if form.is_valid():
                repostajeac = form.save(commit=False)
                tanqueac = repostajeac.reservorio_aceite  # Obtenemos el tanque de aceite relacionado al repostaje

                # Más lógica anti-monos
                if tanqueac.cantidad_aceite + repostajeac.cantidad_repostada > tanqueac.capacidad_aceite:
                    messages.error(request, 'El repostaje excede la capacidad del tanque.')
                    return redirect('repostaje')  # Redirigir de nuevo al formulario de repostaje

                # Si el mono hizo bien el trabajo se guarda
                repostajeac.save()
                tanqueac.cantidad_aceite += repostajeac.cantidad_repostada
                tanqueac.save()

                messages.success(request, 'Repostaje registrado correctamente.')
                return redirect('detalleAceite')  # Redirigir a principal y mono feliz
        else:
            form = RepostajeAceiteForm()
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
    return render(request, 'registrar_repostaje_aceite.html', {'form': form})


def historial_repostaje_aceite(request):
    # Obtener todos los repostajes
    repostajesac = RepostajeAceite.objects.all()
    return render(request, 'historial_repostaje_aceite.html', {'repostajesac': repostajesac})