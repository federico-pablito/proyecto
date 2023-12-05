from django.shortcuts import render
import requests


# Create your views here.
def principal(request):
    official = requests.get("https://dolarapi.com/v1/dolares/oficial").json()
    blue = requests.get("https://dolarapi.com/v1/dolares/blue").json()
    return render(request, 'base.html', {'official_compra': official['compra'], 'official_venta': official['venta'],
                                         'blue_compra': blue['compra'], 'blue_venta': blue['venta']})
