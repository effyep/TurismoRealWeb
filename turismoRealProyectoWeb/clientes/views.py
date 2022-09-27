from multiprocessing import context
from django.shortcuts import render
from .models import Departamentos
from django.db import connection
# Create your views here.

def reservas(request):
    departamentos = Departamentos.objects.all()
    context={
        'departamentos': departamentos
    }
    return render(request, 'clientes/misReservas.html', context)



