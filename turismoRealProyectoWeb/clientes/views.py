import http
from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from django.db import connection
from django.contrib.auth import authenticate
from .models import Departamentos
# Create your views here.

def home(request):
    data ={
    'regiones':listarRegion()
    }

    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

    if request.method == 'POST':
        region = request.POST.get('Regiones')
        personas = request.POST.get('Personas')
        resultados = EncontrarDepto( personas,region)
        data ['resultados']=resultados
        

           
    return render(request, 'clientes/Principal.html', data)



def miPerfil(request):
    data ={
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    return render(request, 'clientes/Perfil.html',data)


def ComoReservar(request):
    data ={
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    return render(request, 'clientes/ComoReservar.html', data)

def reservaExitosa(request):
    return render(request, 'clientes/ReservaExitosa.html')

def detalleParaReservar(request,item):
    
    departamento = Departamentos.objects.get(iddepartamento = item)
    data ={
        'departamento':departamento,
        'depto': datosDepto(item)
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

        
    return render(request, 'clientes/detalleParaReservar.html' ,data)

def solicitarReserva(request):
    data = {
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    return render(request, 'clientes/SolicitarReserva.html',data)

def logout(request):
    try:
        request.session.flush()
        return redirect('iniciarSesion')
    except KeyError:
            pass


def EncontrarDepto(cantidadP, ubicacion):
    cursor = connection.cursor()
    params=( cantidadP,ubicacion)
    cursor.execute('{CALL dbo.SP_C_EncontrarDepto(%s,%s)}', params)
    resultado = cursor.fetchall()
    return resultado

def listarRegion():
    cursor = connection.cursor()
    cursor.execute("{CALL dbo.SP_P_CargarRegion}")
    resultado = cursor.fetchall()
    lista = []
    for c in resultado:
        lista.append(c)

    return lista

def datosDepto(id):
    cursor = connection.cursor()
    params = (id,)
    cursor.execute("{CALL dbo.SP_DATOSDEPTO(%s)}", params)
    resultado = cursor.fetchone()

    return resultado
