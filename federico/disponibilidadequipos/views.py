from django.shortcuts import render, redirect
from .forms import disponibilidad_form
from .filters import disponibilidadfilter
from tablamadre.models import DisponibilidadEquipos, Internos, UnidadesdeProduccion
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.
@login_required
def cargo_disponibilidad(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        if request.method == 'POST':
            form = disponibilidad_form(request.POST)
            if form.is_valid():
                new_disponibilidad = form.save()
                return redirect('main_disponibilidad')
        else:
            form = disponibilidad_form()
        return render(request, 'crear_disponibilidad.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


@login_required
def main_disponibilidad(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        anios = DisponibilidadEquipos.objects.values_list('anio', flat=True).distinct()
        meses_por_anio = {}
        for anio in anios:
            meses = DisponibilidadEquipos.objects.filter(anio=anio).values_list('mes', flat=True).distinct()
            meses_por_anio[anio] = meses
        return render(request, 'main_disponibilidad.html', {'anios': anios, 'meses_por_anio': meses_por_anio})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")



@login_required
def mostrar_disponibilidad(request, anio=None, mes=None):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        filter = disponibilidadfilter(request.GET, queryset=DisponibilidadEquipos.objects.filter(mes=mes, anio=anio))
        if filter.is_valid():
            dataset_mes = transpose_disponibilidad(mes, anio, tabla=filter.qs)
        else:
            dataset_mes = transpose_disponibilidad(mes, anio, tabla=DisponibilidadEquipos.objects.filter(mes=mes, anio=anio))
        columns = ['Int', 'Dueño', 'Operador', 'UP', 'Ingreso Obra', 'Dias Obra']
        for item in range(1, 32):
            columns.append(item)
        columns.append('Dias Trabajados')
        columns.append('Dias No Trabajados')
        return render(request, 'mostrar_disponibilidad.html', {'dataset_mes': dataset_mes, 'columns': columns,
                                                               'mes': mes.title(), 'anio': anio, 'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def transpose_disponibilidad(mes, anio, tabla=None):
    ups = DisponibilidadEquipos.objects.filter(mes=mes, anio=anio).values_list('up', flat=True).distinct()
    dataset = []
    for up in ups:
        tabla1 = tabla.filter(up=UnidadesdeProduccion.objects.get(id=up))
        internos = tabla1.values_list('interno', flat=True).distinct()
        for dato in internos:
            row = []
            row.append(Internos.objects.get(id=dato).interno)
            row.append(Internos.objects.get(id=dato).propietario)
            row.append(tabla.filter(interno=dato, mes=mes, anio=anio).last().chofer)
            row.append(UnidadesdeProduccion.objects.get(id=up).unidadproduccion)
            row.append(tabla.filter(interno=dato, mes=mes, anio=anio).last().fecha_ingreso_de_obra.strftime('%d/%m/%Y'))
            row.append(tabla.filter(interno=dato, mes=mes, anio=anio).last().cantidad_de_dias_en_obra)
            actividad = []
            # Listador de Dias Trabajados
            for item in range(1, 32):
                if item in tabla1.filter(interno=dato, up=UnidadesdeProduccion.objects.get(id=up)).values_list('dia', flat=True):
                    act = tabla1.get(interno=dato, up=UnidadesdeProduccion.objects.get(id=up), dia=item).actividad.categoria
                    row.append(act)
                    actividad.append(act)
                else:
                    row.append(' ')
                    actividad.append(' ')
            # Contador de dias trabajados
            dias_trabajados = 0
            for item in actividad:
                if item.lower() == 'd':
                    dias_trabajados += 1
                else:
                    dias_trabajados += 0
            row.append(dias_trabajados)
            # Dias no trabajados
            row.append(30 - dias_trabajados)
            # Se agrega al dataset
            dataset.append(row)
    return dataset
