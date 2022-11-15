from django.shortcuts import render,redirect
from django.db import connection
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from .models import Usuarios


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

def webpay(request):
    data = {}
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
        idUsuarioActual = request.session['usuario_id']
    return render(request,'clientes/webpay.html')

def miPerfil(request):
    data ={
        
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
        idUsuarioActual = request.session['usuario_id']
        data['id']= mostrarReservas(idUsuarioActual)
        print(data['id'])

    return render(request, 'clientes/Perfil.html',data)

def revisarReserva(request,item):
    usuarioId= request.session['usuario_id']
    data = {
        'reserva': RReserva(item,usuarioId)
        }
    if 'usuario_id' in request.session:
        
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    if request.method == 'POST':
        cancelarReserva(item)
        messages.success(request,"La reserva fue cancelada exitosamente")

        
        
    return render(request, 'clientes/revisarReserva.html',data)

def ComoReservar(request):
    data ={
    }
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
        
    return render(request, 'clientes/ComoReservar.html', data)
    

def listarUsuarios(request):
    data = list(Usuarios.objects.values('usuario','correo','identificacion','celular'))
    return JsonResponse(data, safe = False)



def reservaExitosa(request):
    data = {}
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    return render(request, 'clientes/ReservaExitosa.html')


def detalleParaReservar(request,item):
    data ={
        'depto': datosDepto(item),
        'servicios':datosServicio()
    }
    idUsuario = request.session['usuario_id']
    print(item)
    
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

    

    if request.method == 'POST':
        inicio = request.POST.get('inicio')
        fechaSalida  = request.POST.get('fechaSalida')
        print(inicio)
        print(fechaSalida)
        
        
        cantHuespedes = request.POST.get('Huespedes')
        # trae valores si en algun dia de los seleccionados ya existe una reserva
        disponibilidad =disponibilidadFecha(item,inicio,fechaSalida) 
        print(disponibilidad)
        #trae todos los datos del depto segun la id (q se le pasa por url)
        
        datos = datosDepto(item)
        #aca verificamos si disponibilidad contiene algun valor
        for c in disponibilidad:
            #si la contiene se notifica
            if c[0] != None:
                messages.success(request,f'ya existe una reserva para este departamento entre {c[1]} y {c[2]}, ademas se debe considerar dos dias despues del termino para mantenimiento. por favor, escoge otra fecha')
                break
        else:
            #obtengo una lista de los id's de servicio seleccionados en los input 'checkbox'
            idServicio= request.POST.getlist('servicio')

            print('AAAA',idServicio)
            #aquí comienzo a obtener el valor total de los servicios
            precioTotalServicios =0
            #recorro la lista de id's obtenida anteriormente para obtener el valor de cada servicio 
            for c in idServicio:
                #la funcion consultar servicio se le entrega el id del servicio para obtener todos los datos relacionados a este en una tupla
                #y se guarda el valor en la variable 'valor'
                valor = consultarServicio(c)
                #se actualiza la variable precio sumandole el valor por cada recorrido
                precioTotalServicios = precioTotalServicios+valor[3]
            #desde el procedimiento almacenado extraigo la cantidad de dias 
            
            dias = cantDias(inicio,fechaSalida)
            totalDias= extraerValorTupla(dias,0)
            print('dias',totalDias)
            precioNoche = extraerValorTupla(datos[0],5)
            print(precioNoche)
            precioTotalDias= totalDias*precioNoche
            print('precioTotalDias',precioTotalDias)
            #preio total de la reserva
            precioTotalReserva = precioTotalDias+precioTotalServicios
            print('precioTotalServ',precioTotalServicios)
            #el valor del abono
            abono = calcularAbono(precioTotalReserva)
            #valores q se muestran en el front
            data['abono']=abono
            data['TotalReserva']=precioTotalReserva

            crearPosibleReserva(inicio,fechaSalida,precioNoche,item,idUsuario,precioTotalReserva)
            pr=obtenerIDPosibleReserva(idUsuario)
            pr= extraerValorTupla(pr[0],0)
            data['IDPR']= pr
            

            
            #diccc = {'idServicios':idServicio, 'idDepto':item,'fechas':[fechaLlegada,fechaSalida],'totalDias':totalDias,'precioTotalDias':precioTotalDias,'precioServicios':precioTotalServicios,'precioReserva':precioTotalReserva,'totalAbono':abono}
    return render(request, 'clientes/detalleParaReservar.html' ,data)

def solicitarReserva(request,item):
    data = {
        'datosPosibleReserva': obtenerDatosPosibleReserva(item)
    }
    datosPosibleReserva = obtenerDatosPosibleReserva(item)
    precioTotal = extraerValorTupla(datosPosibleReserva[0],12)
    precioAbono= calcularAbono(precioTotal)
    data['abono'] = precioAbono
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

    if request.method == 'POST':
        
        valor = request.POST.get('total')
        print(valor)
        if valor == precioTotal:
            concretarReservaCompleto(item,valor)
            crearBoletaPagoCompleto('Debito','CHILE','C-'+str(item),valor,item)
            return redirect('webpay')
        
        else:
            concretarReservaAbono(item,valor)
            crearBoletaPagoAbono('Debito','CHILE','C-'+str(item),valor,item)
            return redirect('webpay')



        #print(valor)
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
    cursor.execute("{CALL dbo.SP_RE_CargarRegion}")
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

def mostrarReservas(idUsuario):
    cursor = connection.cursor()
    params =(idUsuario,)
    cursor.execute("{CALL dbo.SP_U_Reservas(%s)}",params)
    resultados = cursor.fetchall()
    return resultados

def RReserva(idReserva,idUsuario):
    cursor = connection.cursor()
    params=(idReserva, idUsuario)
    cursor.execute("{CALL dbo.SP_U_RevisarReserva(%s,%s)}", params)
    resultados = cursor.fetchall()
    return resultados

def servicioExtrasContratados(idUsuario, idReserva):
    cursor = connection.cursor()
    params=(idUsuario,idReserva)
    cursor.execute("{CALL dbo.SP_SEContratados(%s,%s)}",params)
    resultados = cursor.fetchall()
    return resultados
    

def crearPosibleReserva(fechaDesde,fechaHasta,precioNocheDepto,idDepto,idUsuario,precioTotalReserva):
    cursor = connection.cursor()
    params=(fechaDesde,fechaHasta,precioNocheDepto,idDepto,idUsuario,precioTotalReserva)
    cursor.execute("{CALL dbo.SP_CrearPosibleReserva(%s,%s,%s,%s,%s,%s)}",params)

def obtenerIDPosibleReserva(idUsuario):

    cursor = connection.cursor()
    params=(idUsuario,)
    cursor.execute("{CALL dbo.SP_ObtenerIDPosibleReserva(%s)}",params)
    resultado = cursor.fetchall()
    return resultado

def obtenerDatosPosibleReserva(idPosibleReserva):
    cursor = connection.cursor()
    params = (idPosibleReserva,)
    cursor.execute("{CALL dbo.SP_ObtenerDatosPosibleReserva(%s)}",params)
    resultados = cursor.fetchall()
    return resultados

def concretarReservaCompleto(idPosibleReserva, monto):
    cursor = connection.cursor()
    params=(idPosibleReserva,monto)
    cursor.execute("{CALL dbo.SP_ConcretarReservaCompleto(%s,%s)}",params)


def concretarReservaAbono(idPosibleReserva, monto):

    cursor = connection.cursor()
    params=(idPosibleReserva,monto)
    cursor.execute("{CALL dbo.SP_ConcretarReservaAbono(%s,%s)}",params)

def crearBoletaPagoCompleto(medioPago ,banco ,comprobante,monto,idReserva):
    cursor = connection.cursor()
    params=(medioPago ,banco ,comprobante,monto,idReserva)
    cursor.execute("{CALL dbo.SP_CrearBoletaCompleto(%s,%s,%s,%s,%s)}",params)

def crearBoletaPagoAbono(medioPago ,banco ,comprobante,monto,idReserva):
    cursor = connection.cursor()
    params=(medioPago ,banco ,comprobante,monto,idReserva)
    cursor.execute("{CALL dbo.SP_CrearBoletaAbono(%s,%s,%s,%s,%s)}",params)

def cancelarReserva(idReserva):
    cursor=connection.cursor()
    params=(idReserva,)
    cursor.execute("{CALL dbo.SP_CancelarReserva(%s)}",params)