import http
from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from . models import Departamentos
from django.db import connection
from django.contrib.auth import authenticate
# Create your views here.

def home(request):

    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ={
        'regiones':listarRegion(),
        'usuarioActual':usuarioActual}

        if request.method == 'POST':
            region = request.POST.get('Regiones')
            personas = request.POST.get('Personas')
            resultados = EncontrarDepto(region, personas)
            data ['resultados']=resultados
           
    
        return render(request, 'clientes/Principal.html', data)
    
    else:
        return redirect('iniciarSesion')

def resultadosBusqueda(request):
    return render(request, 'clientes/ResultadosBusqueda.html')

def ComoReservar(request):
    return render(request, 'clientes/ComoReservar.html')

def reservaExitosa(request):
    return render(request, 'clientes/ReservaExitosa.html')

def solicitarReserva(request):
    return render(request, 'clientes/SolicitarReserva.html')

def busqueda(request):
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        departamentos = Departamentos.objects.all()
    return render(request, 'clientes/busqueda.html')

def logout(request):
    try:
        request.session.flush()
        return redirect('iniciarSesion')
    except KeyError:
            pass


def EncontrarDepto(ubicacion, cantidadP):
    cursor = connection.cursor()
    params=(ubicacion, cantidadP)
    cursor.execute('{CALL dbo.SP_C_EncontrarDepto(%s,%s)}', params)
    resultado = cursor.fetchall()
    lista = []
    for c in resultado:
        lista.append(c)
    return lista

def listarRegion():
    cursor = connection.cursor()
    cursor.execute("{CALL dbo.SP_P_CargarRegion}")
    resultado = cursor.fetchall()
    lista = []
    for c in resultado:
        lista.append(c)

    return lista
