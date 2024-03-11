from django.shortcuts import render, redirect
from .forms import FormUno, FormDos, FormCombinacion, MotivoRechazoForm
from .models import FormOne, FormTwo, FormCombination
from django.shortcuts import get_object_or_404
from django.http import Http404


def solicitar_traslado(request):
    form_one = FormUno()
    form_two = FormDos()
    form_combination = FormCombinacion()
    form = None  # Inicializar la variable form fuera del bloque condicional

    if request.method == 'POST':
        if 'FormUno' in request.POST:
            form = FormUno(request.POST)
            model = FormOne
            if form.is_valid():
                traslado = form.save(commit=False)
                traslado.solicitante = request.user.username
                traslado.save()
                return redirect('aprobar_traslado', traslado_id=traslado.id)
            # Verificar si el formulario se ha creado y es válido
        elif 'FormDos' in request.POST:
            form = FormDos(request.POST)
            model = FormTwo
            if form.is_valid():
                traslado = form.save(commit=False)
                traslado.solicitante = request.user.username
                traslado.save()
                return redirect('aprobar_traslado', traslado_id=traslado.id)
            # Verificar si el formulario se ha creado y es válido

        elif 'FormCombinacion' in request.POST:
            form = FormCombinacion(request.POST)
            model = FormCombination
            if form.is_valid():
                traslado = form.save(commit=False)
                traslado.solicitante = request.user.username
                traslado.save()
                return redirect('aprobar_traslado', traslado_id=traslado.id)
            # Verificar si el formulario se ha creado y es válido

    return render(request, 'solicitar_traslado.html',
                  {'form_one': form_one, 'form_two': form_two, 'form_combination': form_combination, 'form': form})


def aprobar_traslado(request, traslado_id):
    # Obtener el traslado según su ID
    traslado = None

    try:
        # Intentar obtener el traslado de FormOne
        form_one = get_object_or_404(FormOne, id=traslado_id)
        if form_one:
            traslado = form_one
    except:
        pass

    # Intentar obtener el traslado de FormTwo
    try:
        form_two = FormTwo.objects.get(id=traslado_id)
        if form_two:
            traslado = form_two
    except:
        pass

    try:
        # Intentar obtener el traslado de FormCombination
        form_combination = get_object_or_404(FormCombination, id=traslado_id)
        if form_combination:
            traslado = form_combination
    except:
        pass

    # Verificar si el traslado existe
    if not traslado:
        raise Http404("El traslado solicitado no existe")

    # Si el método es POST, se está enviando el formulario de aprobación/rechazo
    if request.method == 'POST':
        motivo_form = MotivoRechazoForm(request.POST)
        if motivo_form.is_valid():
            motivo = motivo_form.cleaned_data['motivo']
            # Aquí puedes manejar el rechazo del traslado y guardar el motivo
            # Por ejemplo:
            traslado.rechazar(motivo)
            return redirect('solicitudtraslado')  # Redirigir a la página de solicitud de traslado
    else:
        motivo_form = MotivoRechazoForm()  # Crear un formulario vacío para el motivo de rechazo

    return render(request, 'aprobar_traslado.html', {'traslado': traslado, 'motivo_form': motivo_form})