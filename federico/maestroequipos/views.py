from django.shortcuts import render, redirect
from tablamadre.models import Internos, TablaMadre, Reparaciones
from .forms import internosforms
from .filters import internosfilter
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


def mainmaestroequipos(request):
    internos = Internos.objects.all()
    lista_internos, lista_nombres = listador(Internos.objects.all())
    return render(request, 'MainMaestro.html', {'internos': internos, 'lista_nombres': lista_nombres, 'lista_internos': lista_internos})


# Create your views here.
def cargointerno(request):
    internos = Internos.objects.all()
    lista_internos, lista_nombres = listador(Internos.objects.all())
    if request.method == 'POST':
        form = internosforms(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_interno = form.save()
            interno_id = new_interno.id
            up = new_interno.up
            interno_instance = Internos.objects.get(id=interno_id)
            last_reparacion = Reparaciones.objects.filter(interno=interno_id).last()
            if last_reparacion is None:
                last_reparacion = None
            new_tabla_madre = TablaMadre(internos=interno_instance, unidadesdeproduccion=up,
                                         observaciones=descripcion, dolardia=0)
            new_tabla_madre.save()
    else:
        form = internosforms()
    return render(request, 'cargointernos.html', {'internos': internos,
                                                    'form': form, 'lista_internos': lista_internos, 'lista_nombres': lista_nombres})

def filtrointernos(request):
    internos = Internos.objects.all()
    if request.method == 'POST':
        # Si se envió el formulario, procesa los datos
        form = internosforms(request.POST)
        if form.is_valid():
            form.save()
    else:
        # Si no se envió el formulario, crea una instancia del formulario
        form = internosforms()
    filter = internosfilter(request.GET, queryset=internos)
    lista_internos, lista_nombres = listador(filter.qs)
    return render(request, 'filtrointernos.html', { 'form': form,
                                                     'filter': filter, 'lista_internos': lista_internos, 'lista_nombres': lista_nombres})


def editar_interno(request, id=None):
    lista_internos, lista_nombres = listador(Internos.objects.all())
    if id:
        instancia = Internos.objects.get(pk=id)
    else:
        instancia = Interno()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = internosforms(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('main-maestroequipos')
    else:
        form = internosforms(instance=instancia)
    return render(request, 'editar_interno.html', {'form': form, 'lista_internos': lista_internos, 'lista_nombres': lista_nombres})

def internos_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = Internos._meta
    nombres = [campo.name for campo in meta_clase.fields]
    lista_nombres = []
    for nombre in nombres:
        if nombre == 'up':
            lista_nombres.append('up_id')
            lista_nombres.append(nombre)
            lista_nombres.append('ubicacion')
        else:
            lista_nombres.append(nombre)
    return lista_datos, lista_nombres


class internos_pd_view(View):
    def get(self, request, *args, **kwargs):
        internos = Internos.objects.all()
        lista_internos, lista_nombres = listador(internos)
        context = {
            'lista_internos': lista_internos,
            'lista_nombres': lista_nombres,
        }
        pdf = internos_pdf('maestroequipos_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')