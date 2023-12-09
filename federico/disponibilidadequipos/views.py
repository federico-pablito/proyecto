from django.shortcuts import render
from .forms import disponibilidad_form


# Create your views here.
def cargo_disponibilidad(request):
    if request.method == 'POST':
        form = disponibilidad_form(request.POST)
        if form.is_valid():
            new_disponibilidad = form.save()
    else:
        form = disponibilidad_form()
    return render(request, 'crear_disponibilidad.html', {'form': form})