from django.shortcuts import render, redirect
from tablamadre.models import Reparaciones, Internos, TablaMadre
from .forms import reparaciones_form
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .filters import reparaciones_filter

# Create your views here.
def reparaciones_main(request):
    # EL FILTRO NO FUNCIONA, LO USO Y EXPLOTA
    if request.method == 'POST':
        form = reparaciones_form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = reparaciones_form()
    tabla = Reparaciones.objects.all()
    #filter = reparaciones_filter(request.GET, queryset=tabla)
    lista_reparaciones, lista_nombres = listador(tabla)
    #ARREGLAR EL FILTRO
    return render(request, 'reparaciones_main.html', {'form':form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})
def reparaciones_crear(request):
    tabla = Reparaciones.objects.all()
    if request.method == 'POST':
        form = reparaciones_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_reparacion = form.save()
            interno = new_reparacion.interno
            if new_reparacion.estadoreparacion == 'Pendiente':
                new_reparacion.estadoequipo = 'Inoperativo'
            else:
                new_reparacion.estadoequipo = 'Operativo'
            up = Internos.objects.get(id=interno.id).up
            new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         reparaciones=new_reparacion, observaciones=descripcion, dolardia=0)
            new_tabla_madre.save()
    else:
        form = reparaciones_form()
    lista_reparaciones, lista_nombres = listador(tabla)
    return render(request, 'reparaciones_crear.html', {'tabla': tabla, 'form':form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})
def reparaciones_editar(request, id=None):
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
        lista_reparaciones, lista_nombres = listador(tabla)
    return render(request, 'editar_reparaciones.html', {'tabla': tabla, 'form': form, 'lista_reparaciones':lista_reparaciones, 'lista_nombres': lista_nombres})

def reparaciones_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    lista_nombres = ['Id', 'Interno', 'Ubicacion', 'Falla', 'Porcentaje Avance', 'Fecha Reparacion Estimada',
                     'Fecha entrada', 'Fecha Salida', 'Estado Reparacion', 'Estado Equipo']

    return lista_datos, lista_nombres

class reparaciones_pd_view(View):
    def get(self, request, *args, **kwargs):
        reparaciones = Reparaciones.objects.all()
        lista_partes, lista_nombres = listador(reparaciones)
        context = {
            'reparaciones': reparaciones,
            'lista_nombres': lista_nombres,
        }
        pdf = reparaciones_pdf('reparaciones_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
