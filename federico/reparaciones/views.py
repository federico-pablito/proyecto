from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import OrdenDeReparacion, OrdenDeReparacionItem, Reparacion, ParteDiarioMecanicos, MecanicoEncargado
from tablamadre.models import Internos, UnidadesdeProduccion
import requests
from datetime import datetime
from .forms import ReparacionForm, OrdenForm
from django.db import models
from django.http import HttpResponseForbidden
from .filters import reparaciones_filter, ordenes_filter, partes_filter
from utils.modelo_a_excel import model_to_excel
from django.http import HttpResponse


class ReparacionTemporal(models.Model):
    interno = models.CharField(max_length=15, primary_key=True)
    ubicacion = models.CharField(max_length=256, default="Generica")
    supervisor = models.CharField(max_length=256, default="Generica")
    mecanico_encargado = models.CharField(max_length=512)
    falla_general = models.CharField(max_length=512, default="Generica")
    horas_km_entrada = models.CharField(default="Generica", max_length=512)
    fecha_entrada = models.CharField(max_length=512, default="Generica")
    fecha_reparacion = models.CharField(max_length=512, default="Generica")
    estado_reparacion = models.CharField(max_length=512, default="Generica")
    estado_equipo = models.CharField(max_length=512, default="Generica")
    apto_traslado = models.CharField(max_length=512, default="X")
    descripcion = models.CharField(max_length=512, default="Generica")
    orden_reparacion = models.CharField(max_length=512, default="Generica")


class ParteTemporal(models.Model):
    fecha = models.DateField()
    mecanico = models.CharField(max_length=512)
    actividad = models.CharField(max_length=1024)
    horas = models.CharField(max_length=512)


def reparaciones_main(request):
    if request.user.has_perm('reparaciones.puede_ver_reparaciones'):
        tabla = Reparacion.objects.filter(estado_reparacion="Pendiente")
        filter = reparaciones_filter(request.GET, queryset=tabla)
        if filter.is_valid():
            reparaciones = filter.qs
        else:
            reparaciones = tabla
        tabla_temporal = ReparacionTemporal.objects.all()
        tabla_temporal.delete()
        for item in reparaciones:
            try:
                objeto = tabla_temporal.get(interno=item.interno.interno)
                objeto.ubicacion = objeto.ubicacion + "\n" + str(item.taller.nombre)
                objeto.supervisor = objeto.supervisor + "\n" + str(item.supervisor.nombre)
                objeto.mecanico_encargado = objeto.mecanico_encargado + "\n" + str(item.mecanico_encargado.nombre)
                objeto.falla_general = objeto.falla_general + "\n" + item.falla_general
                objeto.horas_km_entrada = objeto.horas_km_entrada + "\n" + str(item.horas_km_entrada.strftime('%d/%m/%Y'))
                objeto.fecha_entrada = objeto.fecha_entrada + "\n" + str(item.fecha_entrada.strftime('%d/%m/%Y'))
                objeto.fecha_reparacion = objeto.fecha_reparacion + "\n" + str(item.fecha_reparacion.strftime('%d/%m/%Y'))
                objeto.estado_reparacion = objeto.estado_reparacion + "\n" + item.estado_reparacion
                objeto.estado_equipo = objeto.estado_equipo + "\n" + item.estado_equipo
                objeto.apto_traslado = objeto.apto_traslado + "\n" + str(item.apto_traslado)
                objeto.descripcion = objeto.descripcion + "\n" + item.descripcion
                objeto.orden_reparacion = objeto.orden_reparacion + "\n" + f"Orden N°{item.orden_reparacion.id}"
                objeto.save()
            except ObjectDoesNotExist:
                tabla_temporal.create(
                    interno=item.interno.interno,
                    ubicacion=item.taller.nombre,
                    supervisor=item.supervisor.nombre,
                    mecanico_encargado=item.mecanico_encargado.nombre,
                    falla_general=item.falla_general,
                    horas_km_entrada=item.horas_km_entrada,
                    fecha_entrada=str(item.fecha_entrada.strftime('%d/%m/%Y')),
                    fecha_reparacion=str(item.fecha_reparacion.strftime('%d/%m/%Y')),
                    estado_reparacion=item.estado_reparacion,
                    estado_equipo=item.estado_equipo,
                    apto_traslado=str(item.apto_traslado),
                    descripcion=item.descripcion,
                    orden_reparacion=f"Orden N°{item.orden_reparacion.id}"
                )
        if 'excel' in request.GET:
           return exportar_reparaciones_filtrado(tabla_temporal)
        return render(request, 'reparaciones_main.html', {'reparaciones': tabla_temporal, 'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_reparacion(request):
    if request.user.has_perm('reparaciones.puede_crear_reparaciones'):
        if request.method == 'POST':
            form = ReparacionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('alguna_url_para_redireccionar')
        else:
            form = ReparacionForm()
        return render(request, 'cargar_reparacion.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def main_ordenes(request):
    if request.user.has_perm('reparaciones.puede_ver_ordenes_reparacion'):
        ordenes = OrdenDeReparacion.objects.all()
        filter = ordenes_filter(request.GET, queryset=ordenes)
        if filter.is_valid():
            ordenes = filter.qs
        else:
            ordenes = OrdenDeReparacion.objects.all()
        for item in ordenes:
            item.items = OrdenDeReparacionItem.objects.filter(orden_de_reparacion=item)
        return render(request, 'main_ordenes.html', {'ordenes': ordenes, 'filter': filter})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def crear_orden(request):
    if request.user.has_perm('reparaciones.puede_crear_ordenes_reparacion'):
        if request.method == 'POST':
            form = OrdenForm(request.POST)
            if form.is_valid():
                up = form.cleaned_data['up']
        else:
            form = OrdenForm()
        items, warehouse_list = obtener_items_de_api()  # This function gets items from the API
        items_not_disc = []
        if request.method == 'POST':
            items_codes = request.POST.getlist('item_code[]')
            cantidades = request.POST.getlist('cantidad[]')
            warehouse_codes = request.POST.getlist('warehouse[]')
            for item_code, cantidad, warehouse_code in zip(items_codes, cantidades, warehouse_codes):
                # Find the item details from the API response
                warehouse_items = items.get(warehouse_code, [])
                item_details = next((item for item in warehouse_items if item['ItemCode'] == item_code), None)
                if item_details:
                    api_response = restar_stock_de_api(item_code, cantidad, warehouse_code, up.unidadproduccion)
                    if api_response and api_response != "Item not Discounted":
                        try:
                            OrdenDeReparacionItem.objects.create(
                                orden_de_reparacion=orden,
                                item_id=item_code,
                                nombre=item_details['ItemName'],
                                cantidad=cantidad,
                                almacen=warehouse_code,
                                # Assuming descripcion is optional, set it to an empty string or a default description
                            )
                        except NameError:
                            orden = OrdenDeReparacion.objects.create(up=up)
                            OrdenDeReparacionItem.objects.create(
                                orden_de_reparacion=orden,
                                item_id=item_code,
                                nombre=item_details['ItemName'],
                                cantidad=cantidad,
                                almacen=warehouse_code,
                                # Assuming descripcion is optional, set it to an empty string or a default description
                            )
                    elif api_response == "Item not Discounted":
                        items_not_disc.append({'item_name': item_details['ItemName'], 'item_code': item_code})
                else:
                    # Handle the case where the item is not found
                    print(f"Item with code {item_code} not found.")
            if len(items_not_disc) == 0:
                return redirect('ordenes')  # Replace with the correct URL
            else:
                if len(items_codes) == len(items_not_disc):
                    procesado = False
                else:
                    procesado = True
                return render(request, 'error_discount.html', {'No_procesado': procesado,
                                                               'items_not_disc': items_not_disc})
        else:
            # Convert the items list to a dictionary for easy access in the template
            return render(request, 'ordenes_reparacion.html', {'items': items, 'form': form,
                                                               'warehouse_list': warehouse_list})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def reparaciones_info(request, interno):
    if request.user.has_perm('reparaciones.puede_ver_reparaciones'):
        interno = Internos.objects.get(interno=interno)
        tabla = Reparacion.objects.filter(interno=interno)
        return render(request, 'reparaciones_info.html', {'reparaciones': tabla, 'interno': interno})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def reparaciones_editar(request, id=None):
    if request.user.has_perm('reparaciones.puede_crear_reparaciones'):
        if id:
            instancia = Reparacion.objects.get(pk=id)
        else:
            instancia = Reparacion()  # Asigna una instancia de alquiler
        if request.method == 'POST':
            form = ReparacionForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return redirect('reparaciones-main')  # Redirige a la página de mostrar alquileres
        else:
            form = ReparacionForm(instance=instancia)
        return render(request, 'cargar_reparacion.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cambiar_estado(request, id=None):
    if request.user.has_perm('reparaciones.puede_ver_reparaciones'):
        reparacion = Reparacion.objects.get(pk=id)
        if reparacion.estadoreparacion == "Pendiente":
            reparacion.estadoreparacion = "Finalizado"
        else:
            reparacion.estadoreparacion = "Pendiente"
        reparacion.save()
        return redirect('reparaciones_info', reparacion.interno.interno)
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def obtener_items_de_api():
    server_url = "https://pablofederico-hanadb.seidor.com.ar:50000"
    username = {'CompanyDB': 'PAFQUA', 'UserName': 'Portal', 'Password': 'PF2024'}
    login_url = f"{server_url}/b1s/v1/Login"
    login_response = requests.post(login_url, json=username)
    items_by_warehouse = {}  # Initialize the dictionary to store items by warehouse
    warehouse_list = []  # Initialize the list to store warehouse codes
    warehouse_list_url = f"{server_url}/b1s/v1/Items('GASOIL')?$select=ItemWarehouseInfoCollection"  # List of warehouses to fetch items from
    if login_response.status_code == 200:
        print("Login successful")
        session = requests.Session()
        warehouse_list = [almacen['WarehouseCode'] for almacen in session.get(warehouse_list_url, cookies=login_response.cookies).json()['ItemWarehouseInfoCollection']]
        for warehouse_code in warehouse_list:
            items_url = f"{server_url}/b1s/v1/$crossjoin(Items,Items/ItemWarehouseInfoCollection)?$expand=Items($select=ItemCode,ItemName),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock)&$filter= Items/ItemCode eq Items/ItemWarehouseInfoCollection/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq '{warehouse_code}'  and Items/ItemWarehouseInfoCollection/InStock ge 1"
            all_items = []  # List to save all items before formatting
            # Fetch and save items data
            while items_url:
                items_response = session.get(items_url, cookies=login_response.cookies)
                if items_response.status_code == 200:
                    items_data = items_response.json()
                    all_items.extend(items_data["value"])

                    # Pagination handling
                    items_url = items_data.get("odata.nextLink", "")
                    if items_url:
                        items_url = f"{server_url}/b1s/v1/{items_url}"
                else:
                    print("Failed to retrieve items for warehouse:", warehouse_code, ". Status code:",
                          items_response.status_code)
                    break

            # Format and save data for the current warehouse
            formatted_items = []
            for item in all_items:
                if item['Items']['ItemCode'] is not None and item['Items']['ItemName'] is not None:
                    formatted_item = {
                        'ItemCode': item['Items']['ItemCode'],
                        'ItemName': item['Items']['ItemName'],
                        'QuantityOnStock': item['Items/ItemWarehouseInfoCollection']['InStock'],
                    }
                    formatted_items.append(formatted_item)

            items_by_warehouse[warehouse_code] = formatted_items

    else:
        print("Login failed. Status code:", login_response.status_code)
    print(items_by_warehouse)
    return items_by_warehouse, warehouse_list


def restar_stock_de_api(item_code, cantidad, warehouse_code, up):
    # Your server details
    server_url = "https://pablofederico-hanadb.seidor.com.ar:50000"
    login_url = f"{server_url}/b1s/v1/Login"
    username = {'CompanyDB': 'PAFQUA', 'UserName': 'Portal', 'Password': 'PF2024'}

    # Login
    login_response = requests.post(login_url, json=username)
    if login_response.status_code == 200:
        session = requests.Session()
        current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        # Create the InventoryGenExit JSON payload
        inventory_exit_payload = {
            "DocDate": current_date,
            "DocDueDate": current_date,
            "Comments": f"Utilizacion en Reparacion - {item_code}",
            "JournalMemo": f"Utilizacion en Reparacion - {item_code}",
            "DocumentLines": [
                {
                    "ItemCode": item_code,
                    "Quantity": float(cantidad),
                    "WarehouseCode": f"{warehouse_code}",
                    "CostingCode": up,
                }
            ],
        }
        # Post the InventoryGenExit request
        inventory_exit_url = f"{server_url}/b1s/v1/InventoryGenExits"
        inventory_exit_response = session.post(inventory_exit_url, json=inventory_exit_payload,
                                               cookies=login_response.cookies)

        if inventory_exit_response.status_code == 201:  # HTTP 201 Created
            print(f"Stock adjustment successful for {item_code}.")
            return True
        if inventory_exit_response.json()['error']['code'] == -10:  # HTTP 400 Bad Request
            return "Item not Discounted"
        else:
            print(f"Failed to adjust stock. Status code: {inventory_exit_response.status_code}")
            return False
    else:
        print(f"Login failed. Status code: {login_response.status_code}")
        return False


def exportar_reparaciones(request):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        queryset = Reparacion.objects.all()

        # No need to manually specify column headers now
        excel_file = model_to_excel(Reparacion, queryset)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Reparaciones.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def exportar_reparaciones_filtrado(reparaciones):
    excel_file = model_to_excel(ReparacionTemporal, reparaciones)

    response = HttpResponse(excel_file,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reparaciones.xlsx"'

    return response


def exportar_reparacion(request, interno=None):
    if request.user.has_perm('tablamadre.puede_ver_reparaciones'):
        reparaciones = Reparacion.objects.filter(interno=Internos.objects.get(interno=interno))

        # No need to manually specify column headers now
        excel_file = model_to_excel(Reparacion, reparaciones)

        response = HttpResponse(excel_file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reparaciones_{interno}.xlsx"'

        return response
    else:
        # Acción a realizar si el usuario no tiene permiso
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def main_parte_mecanicos(request):
    if request.user.has_perm('reparaciones.puede_ver_partes_diarios_mecanicos'):
        if request.user.is_staff:
            tabla = ParteDiarioMecanicos.objects.all()
        else:
            tabla = ParteDiarioMecanicos.objects.filter(mecanico=MecanicoEncargado.objects.get(user=request.user))
        filtro = partes_filter(request.GET, queryset=tabla)
        if filtro.is_valid():
            partes = filtro.qs
        else:
            partes = tabla
        tabla_temporal = ParteTemporal.objects.all()
        tabla_temporal.delete()
        for item in filtro.qs:
            try:
                objeto = tabla_temporal.get(mecanico=item.mecanico.nombre + " " + item.mecanico.apellido, fecha=item.fecha)
                objeto.actividad = objeto.actividad + "\n" + item.actividad
                objeto.horas = objeto.horas + "\n" + f"Cantidad hs {item.horas}"
                objeto.save()
            except ObjectDoesNotExist:
                tabla_temporal.create(
                    fecha=item.fecha,
                    mecanico=item.mecanico.nombre + " " + item.mecanico.apellido,
                    actividad=item.actividad,
                    horas=f"Cantidad hs {item.horas}"
                )
        return render(request, 'main_parte_diario_mecanicos.html', {'partes': tabla_temporal, 'filter': filtro})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")


def cargar_parte_mecanicos(request):
    if request.user.has_perm('reparaciones.puede_crear_partes_diarios_mecanicos'):
        try:
            mecanico = MecanicoEncargado.objects.get(user=request.user)
        except ObjectDoesNotExist:
            mecanico = MecanicoEncargado.objects.get(id=1)
        if request.method == 'POST':
            textos = request.POST.getlist('textos[]')
            cantidades = request.POST.getlist('cantidad[]')
            for texto, cantidad in zip(textos, cantidades):
                if texto != "" and cantidad != "" or cantidad > 0:
                    parte = ParteDiarioMecanicos.objects.create(
                        actividad=texto,
                        horas=cantidad,
                        mecanico=mecanico
                    )
                    parte.save()
            return redirect('main_parte_mecanicos')
        else:
            # Convert the items list to a dictionary for easy access in the template
            return render(request, 'cargar_parte_diario_mecanicos.html',
                          {'mecanico': f'{mecanico.nombre} {mecanico.apellido}',
                           'fecha': datetime.now().strftime('%d/%m/%Y')})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página, haber estudiao.")
