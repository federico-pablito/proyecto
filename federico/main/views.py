from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from tablamadre.models import Internos, Services
from reparaciones.models import Reparacion


@login_required
# Create your views here.
def principal(request):
    user = request.user.first_name + ' ' + request.user.last_name
    permisos = request.user.get_all_permissions()
    official = requests.get("https://dolarapi.com/v1/dolares/oficial").json()
    blue = requests.get("https://dolarapi.com/v1/dolares/blue").json()
    equipos = {'alquilados': Internos.objects.filter(alquilado=True).count(),
              'disponibles': Internos.objects.filter(alquilado=False,actividadvehiculo='DISPONIBLE').count(),
              'activos': Internos.objects.filter(alquilado=False,actividadvehiculo='ACTIVO').count(),
              'inactivos': Internos.objects.filter(alquilado=False,actividadvehiculo='INACTIVO').count()}
    reparaciones_pendientes = Reparacion.objects.filter(estado_reparacion='PENDIENTE').count()
    services = {'normales': Services.objects.filter(necesidadservice='Normal').count(),
                'proximos': Services.objects.filter(necesidadservice='Proximo').count(),
                'excedidos': Services.objects.filter(necesidadservice='Necesita Service').count()
    }

    return render(request, 'base.html', {'official_compra': official['compra'], 'official_venta': official['venta'],
                                         'blue_compra': blue['compra'], 'blue_venta': blue['venta'],
                                         'user': user, 'permisos': permisos, 'equipos': equipos,
                                         'reparaciones_pendientes': reparaciones_pendientes,
                                         'services': services})

