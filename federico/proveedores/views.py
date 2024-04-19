from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import ProveedorForm, EvaluacionProveedorForm
from .models import Proveedor, EvaluacionProveedor
from .filters import EvaluacionFilter

# Create your views here.


def cargar_proveedor(request):
    if request.user.has_perm('proveedores.puede_crear_proveedores'):
        if request.method == 'POST':
            form = ProveedorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('cargar_evaluacion')
        else:
            form = ProveedorForm()
        return render(request, 'cargar_proveedor.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_evaluacion(request):
    if request.user.has_perm('proveedores.puede_crear_evaluaciones_proveedores'):
        if request.method == 'POST':
            form = EvaluacionProveedorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main_evaluacion')
        else:
            form = EvaluacionProveedorForm()
        return render(request, 'cargar_evaluacion.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def main_evaluacion(request):
    if request.user.has_perm('proveedores.puede_ver_evaluaciones_proveedores'):
        evaluaciones = EvaluacionProveedor.objects.all()
        if request.method == 'GET':
            filter = EvaluacionFilter(request.GET, queryset=evaluaciones)
            if filter.is_valid():
                evaluaciones = filter.qs
            else:
                evaluaciones = evaluaciones
        evaluaciones = evaluacion_management(evaluaciones)
        return render(request, 'main_evaluaciones.html', {'evaluaciones': evaluaciones,
                                                          'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def informe_proveedor(request, id_proveedor):
    if request.user.has_perm('proveedores.puede_ver_evaluaciones_proveedores'):
        proveedor = Proveedor.objects.get(id=id_proveedor)
        evaluaciones = EvaluacionProveedor.objects.filter(proveedor=proveedor)
        for item in evaluaciones:
            item.resultado = float(str((item.calidad + item.cumplimiento_plazo_entrega + item.precio_plazo) / 3)[:5])
            item.categoria = 'A' if item.resultado >= 75 else 'B' if item.resultado >= 40 else 'C'
        return render(request, 'informe_proveedor.html', {'evaluaciones': evaluaciones,
                                                          'proveedor': proveedor})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def evaluacion_management(evaluaciones):
    evaluaciones_list = evaluaciones.values_list('proveedor', flat=True).distinct()
    evaluaciones_clases = []
    for item in evaluaciones_list:
        calidad = 0
        cumplimiento_plazo_entrega = 0
        precio_plazo = 0
        id = Proveedor.objects.get(id=item).id
        proveedor = Proveedor.objects.get(id=item).nombre
        for evaluacion in evaluaciones.filter(proveedor=id):
            calidad += evaluacion.calidad
            precio_plazo += evaluacion.precio_plazo
            cumplimiento_plazo_entrega += evaluacion.cumplimiento_plazo_entrega
        calidad = calidad / evaluaciones.filter(proveedor=id).count()
        cumplimiento_plazo_entrega = cumplimiento_plazo_entrega / evaluaciones.filter(proveedor=id
                                                                                      ).count()
        precio_plazo = precio_plazo / evaluaciones.filter(proveedor=id).count()
        resultado = float(str((calidad + cumplimiento_plazo_entrega + precio_plazo) / 3)[:5])
        categoria = 'A' if resultado >= 75 else 'B' if resultado >= 40 else 'C'
        evaluaciones_clases.append(Evaluacion(proveedor, calidad, cumplimiento_plazo_entrega, precio_plazo, resultado,
                                              categoria, id))
    return evaluaciones_clases


class Evaluacion:
    def __init__(self, proveedor, calidad, cumplimiento_plazo_entrega, precio_plazo, resultado, categoria, id):
        self.proveedor = proveedor
        self.calidad = calidad
        self.cumplimiento_plazo_entrega = cumplimiento_plazo_entrega
        self.precio_plazo = precio_plazo
        self.resultado = resultado
        self.categoria = categoria
        self.id = id
