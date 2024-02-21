from django.shortcuts import render, redirect
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from tablamadre.models import Internos, Novedades
from .forms import novedadesforms
from .filters import novedades_filter
from io import BytesIO
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required



class NovedadTemporal(models.Model):
    interno = models.CharField(max_length=15, primary_key=True)
    marca = models.CharField(max_length=256, default="Generica")
    modelo = models.CharField(max_length=512, default="Generico")
    reparado = models.CharField(max_length=512)
    tipo_falla = models.CharField(max_length=512, default="Generica")
    fecha = models.CharField(default="Generica", max_length=512)
    informacion = models.CharField(max_length=512, default="No hay informacion")
    ingreso_hs_km = models.IntegerField(default=1)
    chofer = models.CharField(max_length=512, default="No tiene chofer")


@login_required
def novedades_main(request):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        tabla = Novedades.objects.filter(reparado=False)
        filter = novedades_filter(request.GET, queryset=tabla)
        if filter.is_valid():
            tabla = filter.qs
        tabla_temporal = NovedadTemporal.objects.all()
        tabla_temporal.delete()
        for item in tabla:
            try:
                objeto = tabla_temporal.get(interno=item.interno.interno)
                objeto.reparado = objeto.reparado + "\n" + "X"
                objeto.tipo_falla = objeto.tipo_falla + "\n" + item.tipo_falla
                objeto.informacion = objeto.informacion + "\n" + item.informacion
                objeto.fecha = objeto.fecha + "\n" + str(item.fecha).split(" ")[0]
                objeto.save()
            except ObjectDoesNotExist:
                tabla_temporal.create(
                    interno=item.interno.interno,
                    reparado="X",
                    marca=item.interno.marca,
                    modelo=item.interno.modelo,
                    tipo_falla=item.tipo_falla,
                    fecha=str(item.fecha).split(" ")[0],
                    informacion=item.informacion,
                    ingreso_hs_km=item.ingreso_hs_km,
                    chofer=item.chofer
                )
        return render(request, 'novedades_main.html', {'tabla': tabla_temporal, 'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def novedades_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        if request.method == 'POST':
            form = novedadesforms(request.POST)
            if form.is_valid():
                novedad = form.save(commit=False)
                novedad.reparado = False
                novedad.save()
                return redirect('novedades_main')
        else:
            form = novedadesforms()

        return render(request, 'novedades_crear.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def novedades_info(request, interno):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        interno = Internos.objects.get(interno=interno)
        novedades = Novedades.objects.filter(interno=interno)
        return render(request, 'novedades_info.html', {'novedades': novedades, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def novedades_specifica_crear(request, interno):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        if request.method == 'POST':
            form = novedadesforms(request.POST)
            if form.is_valid():
                novedad = form.save(commit=False)
                novedad.interno = Internos.objects.get(interno=interno)
                novedad.reparado = False
                novedad.save()
                return redirect('novedades_info', interno)
        else:
            form = novedadesforms()

        return render(request, 'novedades_crear.html', {'form': form, 'interno_val': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cambiar_estado(request, id):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        novedad = Novedades.objects.get(id=id)
        novedad.reparado = not novedad.reparado
        novedad.save()
        return redirect('novedades_info', novedad.interno.interno)
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def novedades_detalle(request, id):
    if request.user.has_perm('tablamadre.puede_ver_novedades'):
        novedad = Novedades.objects.get(id=id)
        return render(request, 'novedad_detalle.html', {'novedad': novedad})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")

