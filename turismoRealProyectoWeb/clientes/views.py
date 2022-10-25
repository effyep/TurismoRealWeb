from ast import IsNot
import http
from msilib.schema import CheckBox
from multiprocessing import context
from queue import Empty
from sqlite3 import Cursor
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
        print(resultados)
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
    data ={
        'depto': datosDepto(item),
        'servicios':datosServicio
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

    if request.method == 'POST':
        fechaLlegada = request.POST.get('FechaLlegada')
        fechaSalida = request.POST.get('FechaSalida')
        cantHuespedes = request.POST.get('Huespedes')
        disponibilidad =disponibilidadFecha(item,fechaLlegada,fechaSalida) 
        print(disponibilidad)
        datos = datosDepto(item)
        for c in disponibilidad:
            if c[0] != None:
                data['mensaje']=f'ya existe una reserva para este departamento entre {c[1]} y {c[2]}, ademas se debe considerar dos dias despues del termino para mantenimiento. por favor, escoge otra fecha'
                break
        else:
            #obtengo una lista de los id's de servicio seleccionados en los input 'checkbox'
            idServicio= request.POST.getlist('checkbox')
            print(idServicio)
            #aquí comienzo a obtener el valor total de los servicios
            precioTotalServicios =0
            #recorro la lista de id's obtenida anteriormente para obtener el valor de cada servicio 
            for c in idServicio:
                #la funcion consultar servicio se le entrega el id del servicio para obtener todos los datos relacionados a este en una tupla
                #y se guarda el valor en la variable 'valor'
                valor = consultarServicio(c)
                #se actualiza la variable precio sumandole el valor por cada recorrido
                precioTotalServicios = precioTotalServicios+valor[3]
            print(f'el precio de los servicios es: {precioTotalServicios}')
            
            #desde el procedimiento almacenado extraigo la cantidad de dias 
            dias = cantDias(fechaLlegada,fechaSalida)

            totalDias= extraerValorTupla(dias,0)
            precioNoche = extraerValorTupla(datos[0],5)
            precioTotalDias= totalDias*precioNoche
            print(f'El precio total de los dias es de {precioTotalDias}')
            precioTotalReserva = precioTotalDias+precioTotalServicios
            print(f'el precio total de la reserva es de {precioTotalReserva}')
            abono = calcularAbono(precioTotalReserva)
            print(abono)
            data['abono'] = abono
            data['totalReserva'] = precioTotalReserva
            diccc = {'idServicios':idServicio, 'idDepto':item,'fechas':[fechaLlegada,fechaSalida],'totalDias':totalDias,'precioTotalDias':precioTotalDias,'precioServicios':precioTotalServicios,'precioReserva':precioTotalReserva,'totalAbono':abono}
            print(diccc)
            
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
    resultado = cursor.fetchall()

    return resultado

def datosServicio():
    cursor = connection.cursor()
    cursor.execute("{CALL dbo.SP_MostrarServicios}")
    resultado = cursor.fetchall()
    return resultado

def disponibilidadFecha(ide,Inicio,fin):
    cursor = connection.cursor()
    params=(ide,Inicio,fin)
    cursor.execute("{CALL dbo.SP_C_DisponibilidadFecha(%s,%s,%s)}",params)
    resultado = cursor.fetchall()
    return resultado

def cantDias(Inicio,Fin):
    cursor = connection.cursor()
    params=(Inicio,Fin)
    cursor.execute("{CALL dbo.SP_R_CANTDIAS(%s,%s)}",params)
    resultado = cursor.fetchone()
    return resultado

def extraerValorTupla(tupla,indice):
    for c in tupla:
        valor= tupla[indice]
    return valor

def consultarServicio(id):
    cursor = connection.cursor()
    params =(id,)
    cursor.execute("{CALL dbo.SP_ConsultarServicio(%s)}", params)
    resultado = cursor.fetchone()
    return resultado

def calcularAbono(total):
    abono = round(0.10 * total)
    return abono
    