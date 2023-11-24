from django.shortcuts import render
from django.shortcuts import render, redirect
import templates


def log(request):
     return render(request, 'login.html')
    
    
