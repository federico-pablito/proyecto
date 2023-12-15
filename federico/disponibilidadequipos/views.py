from django.shortcuts import render
from .forms import disponibilidad_form
from tablamadre.models import DisponibilidadEquipos


# Create your views here.
def cargo_disponibilidad(request):
    if request.method == 'POST':
        form = disponibilidad_form(request.POST)
        if form.is_valid():
            new_disponibilidad = form.save()
    else:
        form = disponibilidad_form()
    return render(request, 'crear_disponibilidad.html', {'form': form})


def main_disponibilidad(request):
    return render(request, 'main_disponibilidad.html')


def mostrar_disponibilidad(request, anio=None, mes=None):
    dataset_mes = transpose_disponibilidad(mes, anio)
    columns = ['Interno', 'Propietario', 'Operador', 'Ingreso a Obra', 'Dias en Obra']
    for item in range(1, 32):
        columns.append(item)
    columns.append('Dias Trabajados')
    columns.append('Dias No Trabajados')
    return render(request, 'mostrar_disponibilidad.html', {'dataset_mes': dataset_mes, 'columns': columns,
                                                           'mes': mes.title(), 'anio': anio})


def transpose_disponibilidad(mes, anio):
    ups = DisponibilidadEquipos.objects.filter(mes=mes, anio=anio).values_list('up', flat=True).distinct()
    dataset = []
    for up in ups:
        tabla = DisponibilidadEquipos.objects.filter(mes=mes, up=up)
        internos = tabla.values_list('interno', flat=True).distinct()
        for dato in internos:
            row = []
            row.append(tabla.get(interno=dato).interno.interno)
            row.append(tabla.get(interno=dato).interno.propietario)
            row.append(tabla.get(interno=dato).chofer)
            row.append(tabla.get(interno=dato).fecha_ingreso_de_obra)
            row.append(tabla.filter(interno=dato).last().cantidad_de_dias_en_obra)
            actividad = []
            # Listador de Dias Trabajados
            for item in range(1, 32):
                if item in tabla.filter(interno=dato).values_list('dia', flat=True):
                    act = tabla.filter(dia=item).values_list('actividad', flat=True)
                    a = DisponibilidadEquipos.objects.get(id=act[0])
                    row.append(a.actividad.categoria.upper())
                    actividad.append(act[0])
                else:
                    row.append(' ')
                    actividad.append(' ')
            # Contador de dias trabajados
            dias_trabajados = 0
            for item in actividad:
                if item == 'd':
                    dias_trabajados += 1
                elif item == 'r':
                    dias_trabajados += 0.5
                else:
                    dias_trabajados += 0
            row.append(dias_trabajados)
            # Dias no trabajados
            row.append(30 - dias_trabajados)
            # Se agrega al dataset
            dataset.append(row)
    return dataset
