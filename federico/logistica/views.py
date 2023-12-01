from django.shortcuts import render, redirect
from tablamadre.models import Logistica, Internos, Reparaciones, TablaMadre
from .forms import logistica_form
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Create your views here.
def logistica_main(request):
    logistica = Logistica.objects.all()
    lista_logistica, lista_nombres = listador(logistica)
    tabla_logistica = Logistica.objects.all()
    # HACER EL FILTRO
    return render(request, 'logisticatabla.html', {'lista_logistica': lista_logistica, 'lista_nombres': lista_nombres,'tabla_logistica':tabla_logistica})

def logistica_crear(request):
    if request.method == 'POST':
        form = logistica_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_logistica = form.save()
            interno = new_logistica.interno
            up = Internos.objects.get(id=interno.id).up
            last_reparacion = Reparaciones.objects.filter(interno=interno).last()
            if last_reparacion is None:
                last_reparacion = 1
            new_tabla_madre = TablaMadre(internos=interno, unidadesdeproduccion=up,
                                         logistica=new_logistica, observaciones=descripcion, dolardia=0, reparaciones=last_reparacion)
            new_tabla_madre.save()
            return redirect('logistica_main')
    else:
        form = logistica_form()
    return render(request, 'partediario_crear.html', {'form': form})

def logistica_editar(request):
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
    return render(request, 'partediario_editar.html',
                  {'form': form})
def logistica_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def listador(datos):
    lista_datos = [[dato.id, str(dato).split(', ')] for dato in datos]
    meta_clase = Logistica._meta
    nombres = [campo.name for campo in meta_clase.fields]
    nombres_dependencias = [campo.name for campo in Internos._meta.fields]
    lista_nombres = []
    for nombre in nombres:
        if nombre == 'up':
            lista_nombres.append(nombre)
        else:
            lista_nombres.append(nombre)
    return lista_datos, lista_nombres

class logistica_pdf_view(View):
    def get(self, request, *args, **kwargs):
        logistica = Logistica.objects.all()
        lista_logistica, lista_nombres = listador(logistica)
        context = {
            'tabla_logistica': logistica,
            'lista_nombres': lista_nombres,
        }
        pdf = logistica_pdf('logistica_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')