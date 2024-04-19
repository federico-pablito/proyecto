from django.shortcuts import render, redirect
import requests
from .forms import FormUno,FormCombinacion, FormChoice, SolicitarLogisticaForm
from .models import FormEquipos, FormCombination, SolicitarLogistica
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from .forms import FormCombinacion


def ChooseForm(request):
    if request.method == 'POST':
        form_choice_form = FormChoice(request.POST)
        if form_choice_form.is_valid():
            form_choice = form_choice_form.cleaned_data.get('form_choice')
            if form_choice in ['equipos', 'combination']:  # Verificar que la elección sea válida
                # Redirige a la página de completar formulario.html con el tipo de formulario seleccionado
                return redirect('completar_formulario', form_type=form_choice)
    else:
        form_choice_form = FormChoice()
    
    return render(request, 'choose_form.html', {'form_choice_form': form_choice_form})

def CompletarFormulario(request, form_type=None):
    # Obtener todos los datos necesarios de SAP
    consulta_completa = obtener_id_trasnfer_de_api()
    print("Consulta completa:", consulta_completa)  # Verificar qué se recibe de la API

    # Inicializar form como None para poder asignarle el formulario adecuado más adelante
    form = None

    if form_type == 'equipos':  
        # Lógica para el tipo de formulario 'equipos'
        form = FormUno()  # Crear instancia del formulario FormUno
        print("Creando instancia de FormUno")

        if request.method == 'POST':
            form = FormUno(request.POST)  # Procesar datos del formulario
            print("Datos del formulario POST de FormUno:", request.POST)  # Verificar datos del formulario
            if form.is_valid():
                # Guardar el formulario si es válido
                form.save()
                print("Formulario FormUno válido. Datos guardados.")
                # Redireccionar o mostrar un mensaje de éxito
                return redirect('pablofederico')  # Redirige a la página de éxito o a otra página según necesites

    elif form_type == 'combination':
        if request.method == 'POST':
            # Procesar el formulario con los datos del POST
            form = FormCombinacion(request.POST)
            print("Datos del formulario POST de FormCombinacion:", request.POST)  # Verificar datos del formulario
            if form.is_valid():
                # Guardar el formulario si es válido
                # Aquí accede a los datos del formulario y guarda en tu modelo correspondiente
                id_traslado = form.cleaned_data['id_traslado']
                carreton_propio = form.cleaned_data['carreton_propio']
                equipo_traslada = form.cleaned_data['equipo_traslada']
                proovedor = form.cleaned_data['proovedor']
                tara = form.cleaned_data['tara']
                up_solicita = form.cleaned_data['up_solicita']
                fecha_requeridoobra = form.cleaned_data['fecha_requeridoobra']
                fecha_envio = form.cleaned_data['fecha_envio']
                descripcion = form.cleaned_data['descripcion']
                chofer = form.cleaned_data['chofer']
                valor_viaje = form.cleaned_data['valor_viaje']

                # Crea una instancia del modelo FormCombination y guarda los datos
                form_combination = FormCombination(
                    id_traslado=id_traslado,
                    carreton_propio=carreton_propio,
                    equipo_traslada=equipo_traslada,
                    proovedor=proovedor,
                    tara=tara,
                    up_solicita=up_solicita,
                    fecha_requeridoobra=fecha_requeridoobra,
                    fecha_envio=fecha_envio,
                    descripcion=descripcion,
                    chofer=chofer,
                    valor_viaje=valor_viaje
                )
                form_combination.save()
                
                print("Formulario FormCombinacion válido. Datos guardados.")
                # Redireccionar o mostrar un mensaje de éxito
                return redirect('PabloFederico')  # Redirige a la página de éxito o a otra página según necesites
        else:
            # Crear el formulario con los datos obtenidos de la API
            form = FormCombinacion(consulta_completa=consulta_completa)
            print("Creando instancia de FormCombinacion con consulta completa.")

    if not form:
        # Manejar el caso en que no se haya creado el formulario correctamente
        error_message = "Error al crear el formulario."
        return render(request, 'detalle_form.html', {'error_message': error_message})

    template_name = 'form_uno.html' if form_type == 'equipos' else 'form_combinacion.html'
    return render(request, template_name, {'form': form})

   
def VerForms(request):
    equipos_forms = FormEquipos.objects.all()
    combination_forms = FormCombination.objects.all()

    combination_forms_json = []
    for form in combination_forms:
        form_json = {
            'id': form.id,
            'id_traslado': form.id_traslado,  # Enviamos el campo id_traslado como JSON
            'carreton_propio': form.carreton_propio,
            'equipo_traslada': form.equipo_traslada,
            'proovedor': form.proovedor,
            'tara': form.tara,
            'up_solicita': form.up_solicita,
            'fecha_requeridoobra': form.fecha_requeridoobra,
            'fecha_envio': form.fecha_envio,
            'descripcion': form.descripcion,
            'chofer': form.chofer,
            'valor_viaje': form.valor_viaje,
        }
        combination_forms_json.append(form_json)

    return render(request, 'ver_forms.html', {'equipos_forms': equipos_forms, 'combination_forms_json': combination_forms_json})

def VerDetalle(request, form_id):
    try:
        form_equipos = FormEquipos.objects.get(pk=form_id)
        return render(request, 'detalle_form.html', {'form': form_equipos})
    except FormEquipos.DoesNotExist:
        pass

    try:
        form_combination = FormCombination.objects.get(pk=form_id)
        return render(request, 'detalle_form.html', {'form': form_combination})
    except FormCombination.DoesNotExist:
        pass

    return redirect('ver_forms')


def SolicitarTraslado(request):
    if request.method == 'POST':
        form = SolicitarLogisticaForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            # Redirigir a alguna página de éxito o a donde necesites
            return redirect('ver_solicitudes')
    else:
        form = SolicitarLogisticaForm()
    
    return render(request, 'solicitar_logistica.html', {'form': form})


def VerSolicitudes(request):
    solicitudes = SolicitarLogistica.objects.all()
    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})



def obtener_id_trasnfer_de_api():
    try:
        # URL de la API de SAP
        server_url = "https://pablofederico-hanadb.seidor.com.ar:50000"
        login_url = f"{server_url}/b1s/v1/Login"
        auth_data = {'CompanyDB': 'PAFQUA', 'UserName': 'Portal', 'Password': 'PF2024'}
        login_response = requests.post(login_url, json=auth_data)
        
        if login_response.status_code == 200:
            print("Inicio de sesión exitoso")
            session = requests.Session()
            api_url = f"{server_url}/b1s/v1/$crossjoin(StockTransfers,StockTransfers/StockTransferLines)"
            api_url += "?$expand=StockTransfers($select=DocEntry,DocDate),StockTransfers/StockTransferLines($select=LineNum,ItemCode,ItemDescription,FromWarehouseCode,WarehouseCode,Quantity,Price)"
            api_url += "&$filter=StockTransfers/DocEntry eq StockTransfers/StockTransferLines/DocEntry and StockTransfers/StockTransferLines/FromWarehouseCode eq 'CENTRAL'"
    
            # Realizar la solicitud a la API de SAP
            response = session.get(api_url, cookies=login_response.cookies)
    
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                print("Datos de transferencia obtenidos con éxito")
                # Obtener los datos de la respuesta en formato JSON
                response_data = response.json()
                entities = response_data.get("value", [])
                id_transfers = []
                for item in entities:
                    id_traslado = str(item['StockTransfers']['DocEntry'])
                    quantity = item['StockTransfers/StockTransferLines']['Quantity']
                    item_description = item['StockTransfers/StockTransferLines']['ItemDescription']
                    # Agregar los datos a la lista id_transfers como diccionarios
                    id_transfers.append({
                        'id_traslado': id_traslado,
                        'quantity': quantity,
                        'item_description': item_description
                    })
                
                # Devolver directamente los datos necesarios
                return id_transfers
            else:
                print(f"Error al obtener los datos de transferencia. Código de estado: {response.status_code}")
                return []
            
        else:
            print(f"Fallo en el inicio de sesión. Código de estado: {login_response.status_code}")
            return []
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return []

# Ejemplo de uso
entidades_transf = obtener_id_trasnfer_de_api()
print("Entidades de transferencia obtenidas:")
print(entidades_transf)
