from django.shortcuts import render, redirect
from tablamadre.models import Services, TablaMadre, Internos, Reparaciones
from .forms import service_form
from .filters import service_filter
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
        form = service_form(request.POST)
        if form.is_valid():
            form.save()
    else:
        # Si no se envió el formulario, crea una instancia del formulario
        form = service_form()
    partediario = Services.objects.all()
    parte_filter = service_filter(request.GET, queryset=partediario)
    if parte_filter.is_valid():
        partediario = parte_filter.qs
    order_by = request.GET.get('order_by', 'fechaservicio')
    partediario = partediario.order_by(order_by)
    paginator = Paginator(partediario, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    lista_services, lista_nombres = listador(page_obj)
    # ARREGLAR EL FILTRO
    return render(request, 'service_main.html', {'form': form, 'ilter':parte_filter, 'services':partediario,
                                                'lista_services': lista_services, 'lista_nombres': lista_nombres,})

def editar_serv(request, id=None):
    partediario = Services.objects.all()
    if id:
        instancia = Services.objects.get(pk=id)
    else:
        instancia = Services()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = service_form(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('serviceprin')  # Redirige a la página de mostrar alquileres
    else:
        form = service_form(instance=instancia)
    return render(request, 'editar_service.html', {'partediario': partediario, 'form': form})


def crear_serv(request):
    partediario = Services.objects.all()
    if request.method == 'POST':
        form = service_form(request.POST)
        if form.is_valid():
            new_service = form.save(commit=False)
            new_service.hsxkmrestantes = new_service.proximoservice - new_service.hsxkmactuales
            if new_service.hsxkmrestantes > 50:
                new_service.necesidadservice = 'Normal'
            elif new_service.hsxkmrestantes <= 50:
                new_service.necesidadservice = 'Proximo'
            else:
                new_service.necesidadservice = 'Necesita Service'
            interno = new_service.interno
            up = Internos.objects.get(id=interno.id).up
            last_reparacion = Reparaciones.objects.filter(interno=interno).last()
            descripcion = form.cleaned_data.get('descripcion')
            if last_reparacion is None:
                new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                             observaciones=descripcion)
            else:
                new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         reparaciones=last_reparacion, observaciones=descripcion)
            new_service.save()
            new_tabla_madre.services = new_service
            new_tabla_madre.save()
    else:
        form = service_form()
    lista_services, lista_nombres = listador(partediario)
    return render(request, 'crean_service.html', {'services': partediario, 'form': form,
                                                  'lista_services': lista_services, 'lista_nombres': lista_nombres,})

def service_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = Services._meta
    nombres = [campo.name for campo in meta_clase.fields]
    lista_nombres = []
    for nombre in nombres:
        lista_nombres.append(nombre)
    return lista_datos, lista_nombres

class services_pd_view(View):
    def get(self, request, *args, **kwargs):
        services = Services.objects.all()
        lista_services, lista_nombres = listador(services)
        context = {
            'lista_services': lista_services,
            'lista_nombres': lista_nombres,
        }
        pdf = service_pdf('service_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')