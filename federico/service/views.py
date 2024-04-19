from django.shortcuts import render, redirect
from tablamadre.models import Services, Internos, HistorialService
from .forms import service_form, desplegable_internos
from django.forms.models import model_to_dict
from .filters import servicefilter
from django.core.paginator import Paginator
from io import BytesIO
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
import pandas as pd
from utils.modelo_a_excel import model_to_excel


# Create your views here.
@login_required
def service_main(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        print(actualizacion_warrior())
        if request.method == 'POST':
            # Si se envió el formulario, procesa los datos
            form = desplegable_internos(request.POST)
            if form.is_valid():
                interno = form.cleaned_data['interno']
                try:
                    service = Services.objects.get(interno=interno)
                    return redirect('editar_serv', interno=interno)
                except Services.DoesNotExist:
                    return redirect('create-serv', interno=interno)
        else:
            # Si no se envió el formulario, crea una instancia del formulario
            form = desplegable_internos()
        service = Services.objects.all()
        service_filter = servicefilter(request.GET, queryset=service)
        if service_filter.is_valid():
            service = service_filter.qs
        if 'excel' in request.GET:
           return exportar_services_filtrados(service)
        # ARREGLAR EL FILTRO
        return render(request, 'service_main.html', {'form': form, 'services': service, 'filter': service_filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def actualizacion_warrior():
    services = Services.objects.all()
    a = "No hay servicios para actualizar"
    dataframe = pd.read_csv('service/vehicle_data.csv', sep=',', header=0)
    names = dataframe['vehLabel'].tolist()
    for service in services:
        for item in Services.objects.all().values_list('interno', flat=True):
            if Internos.objects.get(id=item).interno in names:
                a = "Se actualizaron los servicios"
                try:
                    if (dataframe.loc[dataframe['vehLabel'] == service.interno.interno, 'vehOdometro'].iloc[0] >=
                            dataframe.loc[dataframe['vehLabel'] == service.interno.interno, 'vehHorometro'].iloc[0]):
                        service.hsxkmactuales = dataframe.loc[dataframe['vehLabel'] == service.interno.interno, 'vehOdometro'].iloc[0]
                    else:
                        service.hsxkmactuales = dataframe.loc[dataframe['vehLabel'] == service.interno.interno, 'vehHorometro'].iloc[0]
                    service.proximoservice = service.ultimoservice + service.planrealizado_hs
                    service.hsxkmrestantes = service.proximoservice - service.hsxkmactuales
                    if service.hsxkmrestantes > 50:
                        service.necesidadservice = 'Normal'
                    elif 50 >= service.hsxkmrestantes >= 1:
                        service.necesidadservice = 'Proximo'
                    elif service.hsxkmrestantes <= 0:
                        service.necesidadservice = 'Necesita Service'
                    service.save()
                except IndexError:
                    a = "No se encontró el vehículo"
    return a


@login_required
def editar_serv(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        interno = Internos.objects.get(interno=interno)
        partediario = Services.objects.all()
        if id:
            instancia = Services.objects.get(interno=interno.id)
        else:
            instancia = Services()  # Asigna una instancia de alquiler
        if request.method == 'POST':
            form = service_form(request.POST, instance=instancia)
            if form.is_valid():
                service_edit = form.save(commit=False)
                if service_edit.planrealizado == 'HS':
                    service_edit.planrealizado_hs = 250
                elif service_edit.planrealizado == 'KM':
                    service_edit.planrealizado_hs = 10000
                service_edit.proximoservice = service_edit.ultimoservice + service_edit.planrealizado_hs
                service_edit.hsxkmrestantes = service_edit.proximoservice - service_edit.hsxkmactuales
                if service_edit.hsxkmrestantes > 50:
                    service_edit.necesidadservice = 'Normal'
                elif 50 >= service_edit.hsxkmrestantes >= 1:
                    service_edit.necesidadservice = 'Proximo'
                elif service_edit.hsxkmrestantes <= 0:
                    service_edit.necesidadservice = 'Necesita Service'
                service_edit.save()
                HistorialService.objects.create(
                    interno=interno,
                    fechaservicio=service_edit.fechaservicio,
                    fechaparte=service_edit.fechaparte,
                    ultimoservice=service_edit.ultimoservice,
                    planrealizado=service_edit.planrealizado,
                    planrealizado_hs=service_edit.planrealizado_hs,
                    proximoservice=service_edit.proximoservice,
                    hsxkmactuales=service_edit.hsxkmactuales,
                    hsxkmrestantes=service_edit.hsxkmrestantes,
                    necesidadservice=service_edit.necesidadservice,
                    operativo=service_edit.operativo,
                )
                return redirect('serviceprin')  # Redirige a la página de mostrar alquileres
        else:
            form = service_form(instance=instancia)
        return render(request, 'editar_service.html', {'partediario': partediario, 'form': form, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")

@login_required
def crear_serv(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        interno = Internos.objects.get(interno=interno)
        if request.method == 'POST':
            form = service_form(request.POST)
            if form.is_valid():
                new_service = form.save(commit=False)
                new_service.interno = interno
                if new_service.planrealizado == 'HS':
                    new_service.planrealizado_hs = 250
                elif new_service.planrealizado == 'KM':
                    new_service.planrealizado_hs = 10000
                new_service.proximoservice = new_service.ultimoservice + new_service.planrealizado_hs
                new_service.hsxkmrestantes = new_service.proximoservice - new_service.hsxkmactuales
                if new_service.hsxkmrestantes > 50:
                    new_service.necesidadservice = 'Normal'
                elif 50 >= new_service.hsxkmrestantes >= 1:
                    new_service.necesidadservice = 'Proximo'
                elif new_service.hsxkmrestantes <= 0:
                    new_service.necesidadservice = 'Necesita Service'
                new_service.save()
                HistorialService.objects.create(
                    interno=Internos.objects.get(interno=new_service.interno),
                    fechaservicio=new_service.fechaservicio,
                    fechaparte=new_service.fechaparte,
                    ultimoservice=new_service.ultimoservice,
                    planrealizado=new_service.planrealizado,
                    planrealizado_hs=new_service.planrealizado_hs,
                    proximoservice=new_service.proximoservice,
                    hsxkmactuales=new_service.hsxkmactuales,
                    hsxkmrestantes=new_service.hsxkmrestantes,
                    necesidadservice=new_service.necesidadservice,
                    operativo=new_service.operativo,
                )
                return redirect('serviceprin')  # Redirige a la página de mostrar alquileres
        else:
            form = service_form()
        return render(request, 'crean_service.html', {'form': form, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def info_serv(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        interno = Internos.objects.get(interno=interno)
        services = HistorialService.objects.filter(interno=interno)
        return render(request, 'info_service.html', {'services': services, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def services_pdf(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        tabla_temporal = Services.objects.all()
        template_path = 'service_pdf.html'
        template = get_template(template_path)
        html_content = template.render({'services': tabla_temporal})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="output.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_content + '</pre>')
        return response
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_services(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        queryset = Services.objects.all()

        # No need to manually specify column headers now
        excel_file = model_to_excel(Services, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Services.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_services_filtrados(services):
    excel_file = model_to_excel(Services, services)

    response = HttpResponse(excel_file,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Services.xlsx"'

    return response


def exportar_normales(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        queryset = Services.objects.filter(necesidadservice='Normal')

        # No need to manually specify column headers now
        excel_file = model_to_excel(Services, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Services.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_proximos(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        queryset = Services.objects.filter(necesidadservice='Proximo')

        # No need to manually specify column headers now
        excel_file = model_to_excel(Services, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Services.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_necesitan(request):
    if request.user.has_perm('tablamadre.puede_ver_services'):
        queryset = Services.objects.filter(necesidadservice='Necesita Service')

        # No need to manually specify column headers now
        excel_file = model_to_excel(Services, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Services.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")