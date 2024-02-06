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
    # HACER EL FILTRO
    return render(request, 'logisticatabla.html', {'logisticas': logistica})

def logistica_crear(request):
    if request.method == 'POST':
        form = logistica_form(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_logistica = form.save()
            return redirect('logistica_main')
    else:
        form = logistica_form()
    return render(request, 'logistica_crear.html', {'form': form})

def logistica_editar(request, id=None):
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


def logistica_pdf(request):
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
