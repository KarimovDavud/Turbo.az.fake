from django.shortcuts import render, redirect
from .models import Salon

def salons(request):
    salons = Salon.objects.all()
    return render(request, 'salons/salons.html', {'salons': salons})
