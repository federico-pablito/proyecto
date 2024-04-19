from django.shortcuts import render, redirect
from .forms import disponibilidad_form
from .filters import disponibilidadfilter
from tablamadre.models import DisponibilidadEquipos, Internos, UnidadesdeProduccion
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
import pandas as pd


# Create your views here.
@login_required
def cargo_disponibilidad(request):
    if request.user.has_perm('tablamadre.puede_ver_internos'):
        if request.method == 'POST':
            form = disponibilidad_form(request.POST)
            if form.is_valid():
                new_disponibilidad = form.save(commit=False)
                if DisponibilidadEquipos.objects.filter(interno=new_disponibilidad.interno,
                                                        up=new_disponibilidad.up,
                                                        anio=new_disponibilidad.anio,
                                                        mes=new_disponibilidad.mes,
                                                        dia=new_disponibilidad.dia).exists():
                    return render(request, 'crear_disponibilidad.html', {'form': form, 'error': 'Ya hay una disponibilidad cargada de ese dia'})
                else:
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
        for item in range(1, 10):
            columns.append(str(0) + str(item))
        for item in range(10, 32):
            columns.append(item)
        columns.append('Dias Trabajados')
        columns.append('Dias Sin Trabajar')
        columns.append('%')
        if 'excel' in request.GET:
            return exportar_disponibilidad(columns, dataset_mes)
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
            row.append(str(tabla.filter(interno=dato, mes=mes, anio=anio).last().chofer.nombre) +' '+ str(tabla.filter(interno=dato, mes=mes, anio=anio).last().chofer.apellido))
            row.append(UnidadesdeProduccion.objects.get(id=up).unidadproduccion)
            row.append(tabla.filter(interno=dato, mes=mes, anio=anio).last().fecha_ingreso_de_obra.strftime('%d/%m/%Y'))
            row.append(tabla.filter(interno=dato, mes=mes, anio=anio).last().cantidad_de_dias_en_obra)
            actividad = []
            # Listador de Dias Trabajados
            for item in range(1, 32):
                if item in tabla1.filter(interno=dato, up=UnidadesdeProduccion.objects.get(id=up)).values_list('dia', flat=True):
                    act = tabla1.get(interno=dato, up=UnidadesdeProduccion.objects.get(id=up), dia=item, mes=mes, anio=anio).actividad.categoria
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
            row.append(str(dias_trabajados / 30 * 100)[:4])
            # Se agrega al dataset
            dataset.append(row)
    return dataset


def exportar_disponibilidad(cols, df):
    df = pd.DataFrame(df, columns=cols)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Disponibilidad.xls"'
    df.to_excel(response, index=False)
    return response
