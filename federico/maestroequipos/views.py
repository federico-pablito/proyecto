from django.shortcuts import render, redirect
from tablamadre.models import Internos, CertificadosEquiposAlquilados, DisponibilidadEquipos, AlquilerEquipos, \
    FiltrosInternos, NeumaticosInternos, Choferes, Operadores, ArchivosAdjuntos, FotoVehiculos
from .forms import internosforms, AlquilerEquiposForm, CertificadosEquiposAlquiladosForm, FiltroForm, \
    NeumaticoForm, ChoferesForm, OperariosForm, fotosform, adjuntosform
from .filters import internosfilter, alquilerfilter, operadoresfilter, choferesfilter
from io import BytesIO
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from utils.modelo_a_excel import model_to_excel
from django.contrib.auth.models import User
from django.http import FileResponse


@login_required
def mainmaestroequipos(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        internos = Internos.objects.filter(alquilado=False)
        filter = internosfilter(request.GET, queryset=internos)
        if filter.is_valid():
            internos = filter.qs
        valor_total_pesos, valor_total_dolares, valor_total_seguros = get_valores_totales(internos)
        if 'excel' in request.GET:
           return exportar_internos_filtrados(internos)

        return render(request, 'MainMaestro.html',
                      {'internos': internos, 'alquiler': False, 'filter': filter,
                       'valor_total_pesos': valor_total_pesos, 'valor_total_dolares': valor_total_dolares,
                       'valor_total_seguros': valor_total_seguros})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def get_valores_totales(internos):
    valor_total_pesos = 0
    valor_total_dolares = 0
    valor_total_seguros = 0
    for interno in internos:
        valor_total_pesos += interno.valorpesos
        valor_total_dolares += interno.valordolares
        try:
            valor_total_seguros += int(interno.seguro)
        except ValueError:
            valor_total_seguros += 0
    return valor_total_pesos, valor_total_dolares, valor_total_seguros


@login_required
def alquileresinternos(request):
    if request.user.has_perm('tablamadre.puede_ver_alquilados'):
        internos = Internos.objects.filter(alquilado=True)
        filter = alquilerfilter(request.GET, queryset=internos)
        if filter.is_valid():
            internos = filter.qs
        valor_total_pesos, valor_total_dolares, valor_total_seguros = get_valores_totales(internos)

        return render(request, 'MainMaestro.html',
                      {'internos': internos, 'alquiler': True, 'filter': filter,
                       'valor_total_pesos': valor_total_pesos, 'valor_total_dolares': valor_total_dolares,
                       'valor_total_seguros': valor_total_seguros})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


# Create your views here.
@login_required
def cargointerno(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        internos = Internos.objects.all()
        if request.method == 'POST':
            form = internosforms(request.POST, request.FILES)
            if form.is_valid():
                descripcion = form.cleaned_data.pop('descripcion', None)
                new_interno = form.save()
                return redirect('main-maestroequipos')
        else:
            form = internosforms()
        return render(request, 'cargointernos.html', {'internos': internos, 'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def editar_interno(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
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
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def alquilerequipo(request, id=None):
    if request.user.has_perm('tablamadre.puede_ver_alquilados'):
        if request.method == 'POST':
            form = AlquilerEquiposForm(request.POST)
            if form.is_valid():
                nuevo_alquiler = form.save()
                return redirect('main-maestroequipos')
        else:
            form = AlquilerEquiposForm()
        return render(request, 'formulario_alquileres.html',
                      {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def info_interno(request, id):
    if request.user.has_perm('tablamadre.puede_ver_info_internos'):
        internos = Internos.objects.get(id=id)
        if request.method == 'POST':
            form = CertificadosEquiposAlquiladosForm(request.POST)
            if form.is_valid():
                mesanio = form.cleaned_data.pop('fecha', None)
                return redirect('certificado_equipoalquilado', id=id, mesanio=mesanio)
        else:
            form = CertificadosEquiposAlquiladosForm()
        try:
            certificado = AlquilerEquipos.objects.get(interno=internos)
            valor = True
        except:
            valor = False
        choferes = Choferes.objects.filter(interno=internos)
        foto = FotoVehiculos.objects.filter(interno=internos).first()
        return render(request, 'info_interno.html', {'interno': internos, 'form': form, 'formulario': valor,
                                                     'choferes': choferes, 'foto': foto})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def certificado_equipoalquilado(request, id, mesanio):
    if request.user.has_perm('tablamadre.puede_ver_alquilados'):
        mes, anio = mesanio.split(' ')
        interno = Internos.objects.get(id=id)
        certificado = AlquilerEquipos.objects.filter(interno=interno).last()
        try:
            certificado_existente = CertificadosEquiposAlquilados.objects.get(interno=interno, mes=mes, anio=anio)
            return render(request, 'certificado_equipoalquilado.html',
                          {'interno': interno, 'certificado': certificado_existente})
        except CertificadosEquiposAlquilados.DoesNotExist:
            dias_contados = contador_dias_certificado(mes, certificado.up.id, anio, interno.id)
            certificado_existente = CertificadosEquiposAlquilados.objects.create(
                interno=interno,
                contratista=certificado.proveedor,
                mes=mes,
                anio=anio,
                obra=certificado.up,
                periodo_certificado=dias_contados,
                equipo_alquilado=f'{certificado.tipo_vehiculo} {certificado.modelo} {certificado.marca}',
                unidad='Mes',
                certificado_en_mes=round(dias_contados / 30, 2),
                acumulado=round(dias_contados / 30, 2),
                precio_unitario=certificado.monto_contratacion,
                importe=certificado.monto_contratacion*(dias_contados/30),
                total_neto_deducciones=certificado.monto_contratacion*(dias_contados/30),
                total_con_iva=certificado.monto_contratacion*(dias_contados/30)*1.21,)
            certificado_existente = certificado_existente.save()
            return render(request, 'certificado_equipoalquilado.html',
                          {'interno': interno, 'certificado': certificado_existente})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def cargo_filtros(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        if request.method == 'POST':
            form = FiltroForm(request.POST)
            if form.is_valid():
                FiltrosInternos.objects.create(
                    interno=Internos.objects.get(interno=Internos.objects.get(interno=interno)),
                    filtro=form.cleaned_data['filtro'],
                    marca=form.cleaned_data['marca'],
                    codigo=form.cleaned_data['codigo']
                )
                return redirect('mostrar_filtros', interno=interno)
        else:
            form = FiltroForm()
        return render(request, 'cargofiltros.html',
                      {'form': form, 'interno':interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def mostrar_filtros(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        filtros = FiltrosInternos.objects.filter(interno=Internos.objects.get(interno=interno))
        return render(request, 'filtros.html',
                      {'filtros': filtros, 'interno':interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def cargo_neumaticos(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        if request.method == 'POST':
            form = NeumaticoForm(request.POST)
            if form.is_valid():
                NeumaticosInternos.objects.create(
                    interno=Internos.objects.get(interno=Internos.objects.get(interno=interno)),
                    marca=form.cleaned_data['marca'],
                    medida=form.cleaned_data['medida'],
                    codigo=form.cleaned_data['codigo']
                )
                return redirect('mostrar_neumaticos', interno=interno)
        else:
            form = NeumaticoForm()
        return render(request, 'cargoneumaticos.html',
                      {'form': form, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def mostrar_neumaticos(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        neumaticos = NeumaticosInternos.objects.filter(interno=Internos.objects.get(interno=interno))
        return render(request, 'neumaticos.html',
                      {'neumaticos': neumaticos, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_chofer(request):
    if request.user.has_perm('tablamadre.puede_crear_choferes'):
        if request.method == 'POST':
            form = ChoferesForm(request.POST, request.FILES)
            if form.is_valid():
                chofer = form.save(commit=False)
                user_id = form.cleaned_data['usuario'].id  # Assuming 'usuario' is a ModelChoiceField of User model.
                user = User.objects.get(id=user_id)
                chofer.nombre = user.first_name
                chofer.apellido = user.last_name
                chofer = form.save()
                return redirect('main_choferes')
            print(form)
        else:
            form = ChoferesForm()
        return render(request, 'cargar_chofer.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_operario(request):
    if request.user.has_perm('tablamadre.puede_crear_operadores'):
        if request.method == 'POST':
            form = OperariosForm(request.POST, request.FILES)
            if form.is_valid():
                operario = form.save(commit=False)
                user_id = form.cleaned_data['usuario'].id
                user = User.objects.get(id=user_id)
                operario.nombre = user.first_name
                operario.apellido = user.last_name
                operario = form.save()
                return redirect('main_operadores')
        else:
            form = ChoferesForm()
        return render(request, 'cargar_operario.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def main_operadores(request):
    if request.user.has_perm('tablamadre.puede_ver_operadores'):
        operadores = Operadores.objects.all()
        filtro = operadoresfilter(request.GET, queryset=operadores)
        if filtro.is_valid():
            operadores = filtro.qs
        else:
            operadores = operadores
        return render(request, 'main_operadores.html', {'operadores': operadores,
                                                        'filtro': filtro})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def main_choferes(request):
    if request.user.has_perm('tablamadre.puede_ver_operadores'):
        choferes = Choferes.objects.all()
        filtro = choferesfilter(request.GET, queryset=choferes)
        if filtro.is_valid():
            choferes = filtro.qs
        else:
            choferes = choferes
        return render(request, 'main_choferes.html', {'choferes': choferes,
                                                        'filtro': filtro})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def contador_dias_certificado(mes, up, anio, interno_id):
    interno = Internos.objects.get(id=interno_id)
    tabla = DisponibilidadEquipos.objects.filter(mes=mes, anio=anio, up=up, interno=interno)
    actividad = []
    for item in range(1, 32):
        if item in tabla.values_list('dia', flat=True):
            act = tabla.get(dia=item).actividad.categoria
            actividad.append(act)
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


def exportar_internos(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        queryset = Internos.objects.all()

        excel_file = model_to_excel(Internos, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Internos.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_internos_filtrados(internos):
    excel_file = model_to_excel(Internos, internos)

    response = HttpResponse(excel_file,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Internos.xlsx"'

    return response


def cargar_fotos(request):
    if request.user.has_perm('tablamadre.puede_cargar_internos'):
        if request.method == 'POST':
            form = fotosform(request.POST, request.FILES)
            if form.is_valid():
                nueva_foto = form.save()
                return redirect('main-maestroequipos')
        else:
            form = fotosform()
        return render(request, 'cargar_fotos.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_adjuntos(request):
    if request.user.has_perm('tablamadre.puede_cargar_internos'):
        if request.method == 'POST':
            form = adjuntosform(request.POST, request.FILES)
            if form.is_valid():
                nuevo_adjunto = form.save()
                return redirect('main-maestroequipos')
        else:
            form = adjuntosform()
        return render(request, 'cargar_adjuntos.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def ver_adjuntos(request, id):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        interno = Internos.objects.get(id=id)
        adjuntos = ArchivosAdjuntos.objects.filter(interno=interno)
        fotos = FotoVehiculos.objects.filter(interno=interno)
        return render(request, 'ver_adjuntos.html', {'adjuntos': adjuntos, 'fotos': fotos, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
