from django.shortcuts import render, redirect
from tablamadre.models import Services, TablaMadre, Internos, Reparaciones, HistorialService
from .forms import service_form, desplegable_internos
from django.forms.models import model_to_dict
from .filters import servicefilter
from django.core.paginator import Paginator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# Create your views here.
def service_main(request):
    if request.method == 'POST':
        # Si se envió el formulario, procesa los datos
        form = desplegable_internos(request.POST)
        if form.is_valid():
            interno = form.cleaned_data['interno']
            try:
                service = Services.objects.get(interno=interno)
                return redirect('editar_serv', interno=interno)
            except Services.DoesNotExist:
                return redirect('create-serv')
    else:
        # Si no se envió el formulario, crea una instancia del formulario
        form = desplegable_internos()
    service = Services.objects.all()
    service_filter = servicefilter(request.GET, queryset=service)
    if service_filter.is_valid():
        service = service_filter.qs
    # ARREGLAR EL FILTRO
    return render(request, 'service_main.html', {'form': form, 'services': service, 'filter': service_filter})


def editar_serv(request, interno=None):
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
            elif service_edit.hsxkmrestantes <= 50:
                service_edit.necesidadservice = 'Proximo'
            elif service_edit.hsxkmrestantes < 0:
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


def crear_serv(request):
    partediario = Services.objects.all()
    if request.method == 'POST':
        form = service_form(request.POST)
        if form.is_valid():
            new_service = form.save(commit=False)
            if new_service.planrealizado == 'HS':
                new_service.planrealizado_hs = 250
            elif new_service.planrealizado == 'KM':
                new_service.planrealizado_hs = 10000
            new_service.proximoservice = new_service.ultimoservice + new_service.planrealizado_hs
            new_service.hsxkmrestantes = new_service.proximoservice - new_service.hsxkmactuales
            if new_service.hsxkmrestantes > 50:
                new_service.necesidadservice = 'Normal'
            elif new_service.hsxkmrestantes <= 50:
                new_service.necesidadservice = 'Proximo'
            elif new_service.hsxkmrestantes < 0:
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
    return render(request, 'crean_service.html', {'services': partediario, 'form': form})


def info_serv(request, interno=None):
    interno = Internos.objects.get(interno=interno)
    services = HistorialService.objects.filter(interno=interno)
    return render(request, 'info_service.html', {'services': services, 'interno': interno})


def services_pdf(request):
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

