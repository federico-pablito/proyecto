from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import OrdenDeReparacion, OrdenDeReparacionItem, Reparacion
from tablamadre.models import Internos
import requests
from datetime import datetime
from .forms import ReparacionForm
from django.db import models
from django.http import HttpResponseForbidden
from .filters import reparaciones_filter, ordenes_filter


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

        items = obtener_items_de_api()  # This function gets items from the API
        items_not_disc = []
        if request.method == 'POST':
            items_codes = request.POST.getlist('item_code[]')
            cantidades = request.POST.getlist('cantidad[]')
            for item_code, cantidad in zip(items_codes, cantidades):
                # Find the item details from the API response
                item_details = next((item for item in items if item['ItemCode'] == item_code), None)
                if item_details:
                    api_response = restar_stock_de_api(item_code, cantidad, warehouse=item_details['WarehouseCode'])
                    if api_response and api_response != "Item not Discounted":
                        try:
                            OrdenDeReparacionItem.objects.create(
                                orden_de_reparacion=orden,
                                item_id=item_code,
                                nombre=item_details['ItemName'],
                                cantidad=cantidad,
                                # Assuming descripcion is optional, set it to an empty string or a default description
                            )
                        except NameError:
                            orden = OrdenDeReparacion.objects.create()
                            OrdenDeReparacionItem.objects.create(
                                orden_de_reparacion=orden,
                                item_id=item_code,
                                nombre=item_details['ItemName'],
                                cantidad=cantidad,
                                # Assuming descripcion is optional, set it to an empty string or a default description
                            )

                    elif api_response == "Item not Discounted":
                        items_not_disc.append({'item_name': item_details['ItemName'], 'item_code': item_code})
                else:
                    # Handle the case where the item is not found
                    print(f"Item with code {item_code} not found.")
            if len(items_not_disc) == 0:
                return redirect('alguna_url_para_redireccionar')  # Replace with the correct URL
            else:
                if len(items_codes) == len(items_not_disc):
                    procesado = False
                else:
                    procesado = True
                return render(request, 'error_discount.html', {'No_procesado': procesado,
                                                               'items_not_disc': items_not_disc})
        else:
            # Convert the items list to a dictionary for easy access in the template
            return render(request, 'ordenes_reparacion.html', {'items': items})
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
    username = {'CompanyDB': 'PAFTEST', 'UserName': 'Portal', 'Password': '1234'}
    login_url = f"{server_url}/b1s/v1/Login"
    login_response = requests.post(login_url, json=username)
    if login_response.status_code == 200:
        print("Login successful")
        session = requests.Session()
        session_id = login_response.json()["SessionId"]
        login_data = login_response.json()
        items_url = f"{server_url}/b1s/v1/Items?$select=ItemCode,ItemName,QuantityOnStock&$filter=QuantityOnStock ge 1"
        all_items = []
        # Verificar si la solicitud de items fue exitosa
        print()
        while items_url:
            items_response = session.get(items_url, cookies=login_response.cookies)
            print(len(all_items))
            if items_response.status_code == 200:
                items_data = items_response.json()
                all_items.extend(items_data["value"])
                items_url = items_data.get("odata.nextLink")
                if items_url:
                    items_url = f"{server_url}/b1s/v1/{items_url}"
            else:
                print("Failed to retrieve items. Status code:", items_response.status_code)
                break
        sap_values = []
        for item in all_items:
            if item not in sap_values:
                sap_values.append(item)
            else:
                pass
    else:
        sap_values = []
        print("Login failed. Status code:", login_response.status_code)

    # Aquí pondrías tu lógica para conectarte a la API y obtener los ítems
    return sap_values


def restar_stock_de_api(item_code, cantidad, warehouse):
    # Your server details
    server_url = "https://pablofederico-hanadb.seidor.com.ar:50000"
    login_url = f"{server_url}/b1s/v1/Login"
    username = {'CompanyDB': 'PAFTEST', 'UserName': 'Portal', 'Password': '1234'}

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
                    "WarehouseCode": "CENTRAL",
                    "CostingCode": "UP-0",
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

