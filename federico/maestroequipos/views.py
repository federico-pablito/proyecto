from django.shortcuts import render, redirect
from tablamadre.models import Internos, TablaMadre, Reparaciones, CertificadosEquiposAlquilados, DisponibilidadEquipos, AlquilerEquipos
from .forms import internosforms, TableVariable, AlquilerEquiposForm, CertificadosEquiposAlquiladosForm
from .filters import internosfilter
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


def mainmaestroequipos(request):
    internos = Internos.objects.filter(alquilado=False)
    if request.method == 'POST':
        form = TableVariable(request.POST)
        if form.is_valid():
            form_values = {
                'interno_value': form.cleaned_data['interno_value'],
                'marca_value': form.cleaned_data['marca_value'],
                'modelo_value': form.cleaned_data['modelo_value'],
                'tipovehiculo_value': form.cleaned_data['tipovehiculo_value'],
                'chasis_value': form.cleaned_data['chasis_value'],
                'motor_value': form.cleaned_data['motor_value'],
                'dominio_value': form.cleaned_data['dominio_value'],
                'anio_value': form.cleaned_data['anio_value'],
                'aseguradora_value': form.cleaned_data['aseguradora_value'],
                'seguro_value': form.cleaned_data['seguro_value'],
                'seguro_pdf_value': form.cleaned_data['seguro_pdf_value'],
                'itv_value': form.cleaned_data['itv_value'],
                'itv_pdf_value': form.cleaned_data['itv_pdf_value'],
                'titulo_pdf_value': form.cleaned_data['titulo_pdf_value'],
                'tarjeta_value': form.cleaned_data['tarjeta_value'],
                'tarjeta_pdf_value': form.cleaned_data['tarjeta_pdf_value'],
                'propietario_value': form.cleaned_data['propietario_value'],
                'chofer_value': form.cleaned_data['chofer_value'],
                'alquilado_value': form.cleaned_data['alquilado_value'],
                'valorpesos_value': form.cleaned_data['valorpesos_value'],
                'valordolares_value': form.cleaned_data['valordolares_value'],
                'orden_value': form.cleaned_data['orden_value']
            }
            return render(request, 'MainMaestro.html', {'internos': internos, 'form': form,
                                                        'form_values': form_values})
    else:
        form = TableVariable()
    return render(request, 'MainMaestro.html',
                  {'internos': internos,'form': form,
                   'form_values': {'interno_value': True, 'marca_value': True, 'modelo_value': True,
                                   'tipovehiculo_value': True, 'chasis_value': False, 'motor_value': False,
                                   'dominio_value': True, 'anio_value': True, 'aseguradora_value': False,
                                   'seguro_value': False, 'seguro_pdf_value': False, 'itv_value': False,
                                   'itv_pdf_value': False, 'titulo_pdf_value': False, 'tarjeta_value': False,
                                   'tarjeta_pdf_value': False, 'propietario_value': True, 'chofer_value': True,
                                   'alquilado_value': False, 'valorpesos_value': False, 'valordolares_value': False,
                                   'orden_value': True}})


def alquileresinternos(request):
    internos = Internos.objects.filter(alquilado=True)
    if request.method == 'POST':
        form = TableVariable(request.POST)
        if form.is_valid():
            form_values = {
                'interno_value': form.cleaned_data['interno_value'],
                'marca_value': form.cleaned_data['marca_value'],
                'modelo_value': form.cleaned_data['modelo_value'],
                'tipovehiculo_value': form.cleaned_data['tipovehiculo_value'],
                'chasis_value': form.cleaned_data['chasis_value'],
                'motor_value': form.cleaned_data['motor_value'],
                'dominio_value': form.cleaned_data['dominio_value'],
                'anio_value': form.cleaned_data['anio_value'],
                'aseguradora_value': form.cleaned_data['aseguradora_value'],
                'seguro_value': form.cleaned_data['seguro_value'],
                'seguro_pdf_value': form.cleaned_data['seguro_pdf_value'],
                'itv_value': form.cleaned_data['itv_value'],
                'itv_pdf_value': form.cleaned_data['itv_pdf_value'],
                'titulo_pdf_value': form.cleaned_data['titulo_pdf_value'],
                'tarjeta_value': form.cleaned_data['tarjeta_value'],
                'tarjeta_pdf_value': form.cleaned_data['tarjeta_pdf_value'],
                'propietario_value': form.cleaned_data['propietario_value'],
                'chofer_value': form.cleaned_data['chofer_value'],
                'alquilado_value': form.cleaned_data['alquilado_value'],
                'valorpesos_value': form.cleaned_data['valorpesos_value'],
                'valordolares_value': form.cleaned_data['valordolares_value'],
                'orden_value': form.cleaned_data['orden_value']
            }
            return render(request, 'MainMaestro.html', {'internos': internos, 'form': form,
                                                        'form_values': form_values})
    else:
        form = TableVariable()
    return render(request, 'MainMaestro.html',
                  {'internos': internos, 'form': form,
                   'form_values': {'interno_value': True, 'marca_value': True, 'modelo_value': True,
                                   'tipovehiculo_value': True, 'chasis_value': False, 'motor_value': False,
                                   'dominio_value': True, 'anio_value': True, 'aseguradora_value': False,
                                   'seguro_value': False, 'seguro_pdf_value': False, 'itv_value': False,
                                   'itv_pdf_value': False, 'titulo_pdf_value': False, 'tarjeta_value': False,
                                   'tarjeta_pdf_value': False, 'propietario_value': True, 'chofer_value': True,
                                   'alquilado_value': False, 'valorpesos_value': False, 'valordolares_value': False,
                                   'orden_value': True, 'actividad_value': True}})


# Create your views here.
def cargointerno(request):
    internos = Internos.objects.all()
    if request.method == 'POST':
        form = internosforms(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.pop('descripcion', None)
            new_interno = form.save()
    else:
        form = internosforms()
    return render(request, 'cargointernos.html', {'internos': internos, 'form': form})


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
    return render(request, 'filtrointernos.html', {'form': form, 'internos': internos,
                                                   'filter': filter})


def editar_interno(request, id=None):
    internos = Internos.objects.all()
    if id:
        instancia = Internos.objects.get(pk=id)
    else:
        instancia = Internos()  # Asigna una instancia de alquiler
    if request.method == 'POST':
        form = internosforms(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('main-maestroequipos')
    else:
        form = internosforms(instance=instancia)
    return render(request, 'editar_interno.html',
                  {'internos': internos, 'form': form})

def alquilerequipo(request, id=None):
    if request.method == 'POST':
        form = AlquilerEquiposForm(request.POST)
        if form.is_valid():
            nuevo_alquiler = form.save()
            return redirect('main-maestroequipos')
    else:
        form = AlquilerEquiposForm()
    return render(request, 'formulario_alquileres.html',
                  {'form': form})


def info_interno(request, id):
    internos = Internos.objects.all().get(id=id)
    if request.method == 'POST':
        form = CertificadosEquiposAlquiladosForm(request.POST)
        if form.is_valid():
            mesanio = form.cleaned_data.pop('fecha', None)
            return redirect('certificado_equipoalquilado', id=id, mesanio=mesanio)
    else:
        form = CertificadosEquiposAlquiladosForm()
    return render(request, 'info_interno.html', {'interno': internos, 'form': form})


def certificado_equipoalquilado(request, id, mesanio):
    mes, anio = mesanio.split(' ')
    interno = Internos.objects.all().get(id=id)
    certificado = AlquilerEquipos.objects.all().get(tipo_vehiculo=interno.tipovehiculo, modelo=interno.modelo,
                                                    marca=interno.marca)
    try:
        certificado_existente = CertificadosEquiposAlquilados.objects.get(
            equipo_alquilado=f'{certificado.tipo_vehiculo} {certificado.modelo} {certificado.marca}',
            mes=mes, anio=anio)
        return render(request, 'certificado_equipoalquilado.html',
                      {'interno': interno, 'certificado': certificado_existente})
    except CertificadosEquiposAlquilados.DoesNotExist:
        dias_contados = contador_dias_certificado(mes, certificado.up.id, anio, certificado.dominio, interno.id)
        CertificadosEquiposAlquilados.objects.create(
            contratista=certificado.proveedor,
            mes=mes,
            anio=anio,
            obra=certificado.up,
            periodo_certificado=dias_contados,
            equipo_alquilado=f'{certificado.tipo_vehiculo} {certificado.modelo} {certificado.marca}',
            unidad='Mes',
            certificado_en_mes=round(dias_contados / 30, 2),
            acumulado = round(dias_contados / 30, 2),
            precio_unitario=certificado.monto_contratacion,
            importe=certificado.monto_contratacion*(dias_contados/30),
            total_neto_deducciones=certificado.monto_contratacion*(dias_contados/30),
            total_con_iva=certificado.monto_contratacion*(dias_contados/30)*1.21,)
        certificado_existente = CertificadosEquiposAlquilados.objects.get(
            equipo_alquilado=f'{certificado.tipo_vehiculo} {certificado.modelo} {certificado.marca}',
            mes=mes, anio=anio)
        return render(request, 'certificado_equipoalquilado.html',
                      {'interno': interno, 'certificado': certificado_existente})


def internos_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class internos_pd_view(View):
    def get(self, request, *args, **kwargs):
        internos = Internos.objects.all()
        context = {
            'internos': internos,
        }
        pdf = internos_pdf('maestroequipos_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

def contador_dias_certificado(mes, up, anio, dominio, interno_id):
    interno = Internos.objects.get(id=interno_id)
    tabla = DisponibilidadEquipos.objects.filter(mes=mes, anio=anio, up=up, interno=interno)
    actividad = []
    for item in range(1, 32):
        if item in tabla.filter(interno=interno).values_list('dia', flat=True):
            act = tabla.filter(dia=item).values_list('actividad', flat=True)
            a = DisponibilidadEquipos.objects.get(id=act[0])
            actividad.append(a.actividad.categoria)
        else:
            actividad.append(' ')
    # Contador de dias trabajados
    dias_trabajados = 0
    for item in actividad:
        if item == 'd':
            dias_trabajados += 1
        elif item == '2':
            dias_trabajados += 0.5
        else:
            dias_trabajados += 0
    return dias_trabajados
