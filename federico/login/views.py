from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect



@ensure_csrf_cookie
def inicio_view(request):
    if request.user.is_authenticated:
        return redirect('pablofederico')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('pablofederico')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
