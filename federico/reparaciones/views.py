from django.shortcuts import render, redirect
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from tablamadre.models import Reparaciones, Internos, TablaMadre
from .filters import reparaciones_filter
from .forms import reparaciones_form
from io import BytesIO
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required


class ReparacionTemporal(models.Model):
    interno = models.CharField(max_length=15, primary_key=True)
    ubicacion = models.CharField(max_length=256, default="Generica")
    mecanico_encargado = models.CharField(max_length=512)
    falla_general = models.CharField(max_length=512, default="Generica")
    fechareparacionestimada = models.CharField(default="Generica", max_length=512)
    fechaentrada = models.CharField(max_length=512, default="Generica")
    fechasalida = models.CharField(max_length=512, default="Generica")
    estadoreparacion = models.CharField(max_length=512, default="Generica")
    estadoequipo = models.CharField(max_length=512, default="Generica")
    apto_traslado = models.CharField(max_length=512, default="X")
    descripcion = models.CharField(max_length=512, default="Generica")


@login_required
def reparaciones_main(request):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        tabla = Reparaciones.objects.filter(estadoreparacion="Pendiente")
        filter = reparaciones_filter(request.GET, queryset=tabla)
        if filter.is_valid():
            reparaciones = filter.qs
        tabla_temporal = ReparacionTemporal.objects.all()
        tabla_temporal.delete()
        for item in reparaciones:
            try:
                objeto = tabla_temporal.get(interno=item.interno.interno)
                objeto.ubicacion = objeto.ubicacion + "\n" + str(item.taller.nombre)
                objeto.mecanico_encargado = objeto.mecanico_encargado + "\n" + str(item.mecanico_encargado.nombre)
                objeto.falla_general = objeto.falla_general + "\n" + item.falla_general
                objeto.fechareparacionestimada = objeto.fechareparacionestimada + "\n" + str(item.fechareparacionestimada.strftime('%d/%m/%Y'))
                objeto.fechaentrada = objeto.fechaentrada + "\n" + str(item.fechaentrada.strftime('%d/%m/%Y'))
                objeto.fechasalida = objeto.fechasalida + "\n" + str(item.fechasalida.strftime('%d/%m/%Y'))
                objeto.estadoreparacion = objeto.estadoreparacion + "\n" + item.estadoreparacion
                objeto.estadoequipo = objeto.estadoequipo + "\n" + item.estadoequipo
                objeto.apto_traslado = objeto.apto_traslado + "\n" + str(item.apto_traslado)
                objeto.descripcion = objeto.descripcion + "\n" + item.descripcion
                objeto.save()
            except ObjectDoesNotExist:
                tabla_temporal.create(
                    interno=item.interno.interno,
                    ubicacion=item.taller.nombre,
                    mecanico_encargado=item.mecanico_encargado.nombre,
                    falla_general=item.falla_general,
                    fechareparacionestimada=str(item.fechareparacionestimada.strftime('%d/%m/%Y')),
                    fechaentrada=str(item.fechaentrada.strftime('%d/%m/%Y')),
                    fechasalida=str(item.fechasalida.strftime('%d/%m/%Y')),
                    estadoreparacion=item.estadoreparacion,
                    estadoequipo=item.estadoequipo,
                    apto_traslado=str(item.apto_traslado),
                    descripcion=item.descripcion
                )

        return render(request, 'reparaciones_main.html', {'reparaciones': tabla_temporal, 'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def reparaciones_info(request, interno):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        interno = Internos.objects.get(interno=interno)
        tabla = Reparaciones.objects.filter(interno=interno)
        return render(request, 'reparaciones_info.html', {'tabla': tabla, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def reparaciones_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        tabla = Reparaciones.objects.all()
        if request.method == 'POST':
            form = reparaciones_form(request.POST)
            if form.is_valid():
                Reparaciones.objects.create(
                    interno=form.cleaned_data['interno'],
                    taller=form.cleaned_data['taller'],
                    mecanico_encargado=form.cleaned_data['mecanico_encargado'],
                    falla_general=form.cleaned_data['falla_general'],
                    fechareparacionestimada=form.cleaned_data['fechareparacionestimada'],
                    fechaentrada=form.cleaned_data['fechaentrada'],
                    fechasalida=form.cleaned_data['fechasalida'],
                    estadoreparacion=form.cleaned_data['estadoreparacion'],
                    estadoequipo=form.cleaned_data['estadoequipo'],
                    apto_traslado=form.cleaned_data['apto_traslado'],
                    descripcion=form.cleaned_data['descripcion'],
                )
                return redirect('reparaciones-main')
        else:
            form = reparaciones_form()
        return render(request, 'reparaciones_crear.html', {'tabla': tabla, 'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def reparaciones_editar(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
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
        return render(request, 'editar_reparaciones.html', {'tabla': tabla, 'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cambiar_estado(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        reparacion = Reparaciones.objects.get(pk=id)
        if reparacion.estadoreparacion == "Pendiente":
            reparacion.estadoreparacion = "Finalizado"
        else:
            reparacion.estadoreparacion = "Pendiente"
        reparacion.save()
        return redirect('reparaciones_info', reparacion.interno.interno)
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")

@login_required
def reparaciones_pdf(request):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        tabla_temporal = ReparacionTemporal.objects.all()
        template_path = 'reparaciones_pdf.html'
        template = get_template(template_path)
        html_content = template.render({'tabla': tabla_temporal})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="output.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_content + '</pre>')
        return response
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
