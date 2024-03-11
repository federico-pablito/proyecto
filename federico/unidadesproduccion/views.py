from django.shortcuts import render
from tablamadre.models import UnidadesdeProduccion
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from utils.modelo_a_excel import model_to_excel
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def verunidadproduccion(request):
    meta_clase = UnidadesdeProduccion._meta
    nombres = [campo.name for campo in meta_clase.fields]
    tabla = UnidadesdeProduccion.objects.all()
    lista_unidadesp, lista_nombres = listador(tabla)
    return render(request, 'holaquease.html',
                  {'tabla': tabla, 'nombres': nombres, 'lista_unidadesp': lista_unidadesp, 'lista_nombres': lista_nombres})

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
    nombres = [campo.name.capitalize() for campo in meta_clase.fields]
    nombres[1] = 'Unidad de Produccion'
    lista_nombres = nombres
    return lista_datos, lista_nombres

class unidades_pdf_view(View):
    def get(self, request, *args, **kwargs):
        unidad_produccion = UnidadesdeProduccion.objects.all()
        lista_unidadesp, lista_nombres = listador(unidad_produccion)
        context = {
            'lista_unidadesp': lista_unidadesp,
            'lista_nombres': lista_nombres,
            'tabla': unidad_produccion,
        }
        pdf = unidadproduccion_pdf('unidades_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


@login_required
def exportar_ups(request):
    queryset = UnidadesdeProduccion.objects.all()

    # No need to manually specify column headers now
    excel_file = model_to_excel(UnidadesdeProduccion, queryset)

    response = HttpResponse(excel_file,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="UnidadesdeProducion.xlsx"'

    return response
