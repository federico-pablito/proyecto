from django.shortcuts import render, redirect
from tablamadre.models import PartesDiarios, Internos, Reparaciones, TablaMadre
from .forms import partediario_form
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# Create your views here.
def partesdiario_main(request):
    partediario = PartesDiarios.objects.all()
    lista_partediario, lista_nombres = listador(partediario)
    # HACER EL FILTRO
    return render(request, 'partediario_main.html',
                  {'lista_partediario': lista_partediario, 'lista_nombres': lista_nombres, 'parte': partediario})


def partediario_crear(request):
    if request.method == 'POST':
        form = partediario_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_parte = form.save()
            interno = new_parte.interno
            up = Internos.objects.get(id=interno.id).up
            last_reparacion = Reparaciones.objects.filter(interno=interno.id).last()
            if last_reparacion is None:
                last_reparacion = Reparaciones.objects.first()
            new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         partesdiarions=new_parte, observaciones=descripcion, dolardia=0, reparaciones=last_reparacion)
            new_tabla_madre.save()
            return redirect('partesdiario_main')
    else:
        form = partediario_form()
    return render(request, 'partediario_crear.html', {'form': form})


def partediario_editar(request):
    if id:
        instancia = PartesDiarios.objects.get(pk=id)
    else:
        instancia = PartesDiarios()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = partediario_form(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('partesdiario_main')
    else:
        form = partediario_form(instance=instancia)
    return render(request, 'partediario_editar.html',
                  { 'form': form})


def partes_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = PartesDiarios._meta
    nombres = [campo.name for campo in meta_clase.fields]
    lista_nombres = []
    for nombre in nombres:
        lista_nombres.append(nombre)
    return lista_datos, lista_nombres


class partes_pd_view(View):
    def get(self, request, *args, **kwargs):
        partediario = PartesDiarios.objects.all()
        lista_partes, lista_nombres = listador(partediario)
        context = {
            'parte': partediario,
            'lista_nombres': lista_nombres,
        }
        pdf = partes_pdf('partediario_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
