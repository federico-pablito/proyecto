from django.shortcuts import render, redirect
from .models import OrdenDeReparacion, OrdenDeReparacionItem
import requests
from datetime import datetime
# Create your views here.


def crear_orden(request):
    items = obtener_items_de_api()  # This function gets items from the API
    items_not_disc = []
    if request.method == 'POST':
        items_codes = request.POST.getlist('item_code[]')
        cantidades = request.POST.getlist('cantidad[]')
        for item_code, cantidad in zip(items_codes, cantidades):
            # Find the item details from the API response
            item_details = next((item for item in items if item['ItemCode'] == item_code), None)
            if item_details:
                api_response = restar_stock_de_api(item_code, cantidad)
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
        items_url = f"{server_url}/b1s/v1/Items?$select=ItemCode,ItemName,QuantityOnStock&$filter= QuantityOnStock ge 1"
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


def restar_stock_de_api(item_code, cantidad):
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

