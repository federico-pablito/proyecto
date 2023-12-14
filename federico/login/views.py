from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def inicio_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('pablofederico')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    
