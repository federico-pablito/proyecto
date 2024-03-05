from django.shortcuts import render, redirect
from tablamadre.models import Logistica, Internos, RequerimientoEquipo, RequerimientoTraslado, Cronogroma
from .forms import logistica_form, requerimiento_equipo_form, requerimiento_traslado_form, cronograma_form
from io import BytesIO
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def logistica_main(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        logistica = Logistica.objects.all()
        # HACER EL FILTRO
        return render(request, 'logisticatabla.html', {'logisticas': logistica})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")



@login_required
def logistica_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        if request.method == 'POST':
            form = logistica_form(request.POST)
            if form.is_valid():
                descripcion = form.cleaned_data.pop('descripcion', None)
                new_logistica = form.save()
                return redirect('logistica_main')
        else:
            form = logistica_form()
        return render(request, 'logistica_crear.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")



@login_required
def logistica_editar(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        if id:
            instancia = Logistica.objects.get(pk=id)
        else:
            instancia = Logistica()  # Asigna una instancia de alquiler
        if request.method == 'POST':
            form = logistica_form(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return redirect('logistica_main')
        else:
            form = logistica_form(instance=instancia)
        return render(request, 'logistica_editar.html',
                      {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")



@login_required
def requerimiento_equipo_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        if request.method == 'POST':
            form = requerimiento_equipo_form(request.POST)
            if form.is_valid():
                new_requerimiento = form.save()
                return redirect('requerimiento_equipo_mostrar')
        else:
            form = requerimiento_equipo_form()
        return render(request, 'requerimiento_equipo_crear.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def requerimiento_equipo_mostrar(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoEquipo.objects.all()
        return render(request, 'requerimiento_equipo_mostrar.html', {'requerimientos': requerimiento})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")



@login_required
def requerimiento_equipo_info(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoEquipo.objects.get(pk=id)
        return render(request, 'requerimiento_equipo_info.html',
                      {'requerimiento': requerimiento})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def requerimiento_equipo_aprobar(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoEquipo.objects.get(pk=id)
        if requerimiento.aprobado:
            requerimiento.aprobado = False
        else:
            requerimiento.aprobado = True
        requerimiento.save()
        return redirect('requerimiento_equipo_info', id=id)
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def requerimiento_traslado_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        if request.method == 'POST':
            form = requerimiento_traslado_form(request.POST)
            if form.is_valid():
                new_requerimiento = form.save()
                return redirect('requerimiento_traslado_mostrar')
        else:
            form = requerimiento_traslado_form()
        return render(request, 'requerimiento_traslado_crear.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def requerimiento_traslado_mostrar(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoTraslado.objects.all()
        return render(request, 'requerimiento_traslado_mostrar.html', {'requerimientos': requerimiento})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def requerimiento_traslado_info(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoTraslado.objects.get(pk=id)
        return render(request, 'requerimiento_traslado_info.html',
                      {'requerimiento': requerimiento})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def requerimiento_traslado_aprobar(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        requerimiento = RequerimientoTraslado.objects.get(pk=id)
        if requerimiento.aprobado:
            requerimiento.aprobado = False
        else :
            requerimiento.aprobado = True
        requerimiento.save()
        return render(request, 'requerimiento_traslado_info.html',
                      {'requerimiento': requerimiento})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def cronograma_crear(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        if request.method == 'POST':
            form = cronograma_form(request.POST)
            if form.is_valid():
                new_cronograma = form.save()
                return redirect('cronograma_mostrar')
        else:
            form = cronograma_form()
        return render(request, 'cronograma_crear.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def cronograma_mostrar(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        cronograma = Cronogroma.objects.all()
        return render(request, 'cronograma_mostrar.html', {'cronogramas': cronograma})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def logistica_pdf(request):
    if request.user.has_perm('tablamadre.puede_ver_logistica'):
        tabla_temporal = Logistica.objects.all()
        template_path = 'logistica_pdf.html'
        template = get_template(template_path)
        html_content = template.render({'logisticas': tabla_temporal})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="output.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_content + '</pre>')
        return response
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
