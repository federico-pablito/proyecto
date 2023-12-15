from django.shortcuts import render
from tablamadre.models import UnidadesdeProduccion
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
def verunidadproduccion(request):
    meta_clase = UnidadesdeProduccion._meta
    nombres = [campo.name for campo in meta_clase.fields]
    tabla = UnidadesdeProduccion.objects.all()
<<<<<<< Updated upstream
    lista_unidadesp, lista_nombres = listador(tabla)
    return render(request, 'holaquease.html', {'tabla': tabla, 'nombres': nombres, 'lista_unidadesp': lista_unidadesp, 'lista_nombres': lista_nombres,})
=======
    lista_unidadesp, lista_nombres = listador(tabla) 
    return render(request, 'holaquease.html',
                  {'tabla': tabla, 'nombres': nombres, 'lista_unidadesp': lista_unidadesp, 'lista_nombres': lista_nombres})
   
>>>>>>> Stashed changes

def unidadproduccion_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = UnidadesdeProduccion._meta
    nombres = [campo.name for campo in meta_clase.fields]
    lista_nombres = nombres
    return lista_datos, lista_nombres

class unidades_pdf_view(View):
    def get(self, request, *args, **kwargs):
        unidad_produccion = UnidadesdeProduccion.objects.all()
        lista_unidadesp, lista_nombres = listador(unidad_produccion)
        context = {
            'lista_unidadesp': lista_unidadesp,
            'lista_nombres': lista_nombres,
        }
        pdf = unidadproduccion_pdf('unidades_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')