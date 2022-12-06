import random
from django.shortcuts import render,redirect
from django.db import connection
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from .models import Usuarios, Detalleservicio
from transbank.webpay.webpay_plus.transaction import *
from transbank.common.options import *
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import datetime

def enviarmailBoleta(correo,amount,depto,fechaT,tipoTarjeta,fechaD,fechaH,nombreDepto,direccionDepto,comunaDepto,regionDepto,digitos):
    contexto={'correo':correo,
                'amount':amount,
                'depto':depto,
                'fechaT':fechaT,
                'fechaD':fechaD,
                'fechaH':fechaH,
                'tipoTarjeta':tipoTarjeta,
                'nombreDepto':nombreDepto,
                'direccionDepto':direccionDepto,
                'comunaDepto':comunaDepto,
                'regionDepto':regionDepto,
                '4digitos': digitos
                }

    template = get_template("clientes/correoBoleta.html")
    content = template.render(contexto)

    email= EmailMultiAlternatives(
        'Confirmación de reserva',
        'TurismoReal',
        settings.EMAIL_HOST_USER,
        [correo]
    )
    email.attach_alternative(content,'text/html')
    email.send()
    

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
    usuarioActual = request.session.get("usuario_id")
    if usuarioActual is None:
        return redirect('home')
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
        idUsuarioActual = request.session['usuario_id']
        data['id']= mostrarReservas(idUsuarioActual)
        print(data['id'])

    if not data['id']:
        messages.success(request,"No tienes ninguna reserva aún, puedes comenzar en cualquier minuto.")
    
    

    return render(request, 'clientes/Perfil.html',data)

def revisarReserva(request,item):
    usuarioActual = request.session.get("usuario_id")
    if usuarioActual is None:
        return redirect('home')
    usuarioId= request.session['usuario_id']
    data = {
        
        }
    if 'usuario_id' in request.session:
        data['reservas']= RReserva(item)
        data['servicios']= servicioExtrasContratados(item,usuarioId)
        print(data['reservas'])

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
    bolsa = request.session.get('bolsa')
    ##Esta variable es entregada por transbank en caso de haber un problema con el pago
    tbk=request.GET.get('TBK_ORDEN_COMPRA')
    #si hay un problema o en la sesion no existe una bolsa entonces redireccione a la vista anterior
    if tbk :
        return redirect('confirmarReserva')
    
    if bolsa is None:
        return redirect('home')
    bolsa = request.session['bolsa']

    idDepto = bolsa['idDepartamento']
    
    idUsuario = request.session['usuario_id']
    u = Usuarios.objects.filter(idusuario = idUsuario).values()
    correoUsuario=u[0]['correo']

    data = {
        ##funcion que me trae toda la info del departamento pasandole la id
        'depto': datosDepto(idDepto)
    }
    
    ##de la bolsa extraigo el id del departamento
    
    ##aqui puedo sacar info del depto en si
    ##nombre depto
    nombreDepto = data['depto'][0][1]
    ##direccion
    direccionDepto=data['depto'][0][2]
    ##comuna
    comunaDepto =data['depto'][0][10]
    ##region
    regionDepto =data['depto'][0][11]

    
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    
        resultado=request.GET.get('token_ws')
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        resp = tx.commit(resultado)
        fechaD=bolsa['fechaDesde']
        fechaH=bolsa['fechaHasta']
        data['respuesta'] = resp
        data['nombreDepto']= nombreDepto
        fechahora= resp['transaction_date']
        fechaT= fechahora[0:10]
        infoPosibleReserva = request.session['infoPosibleReserva']
        print(infoPosibleReserva)
        id=infoPosibleReserva['idPosibleReserva']
        print(id)
        monto =resp['amount']
        digitos = resp['card_detail']['card_number']
        status=str(resp['status'])
        order=str(resp['buy_order'])
        payment_type_code = str(resp['payment_type_code'])
        tipoDePago = {'VD':'Venta Debito','VN':'Venta Normal','VC':'Venta en cuotas','VP':'Venta Prepago'}
        formaPago = tipoDePago.get(payment_type_code)
        data['tipoTarjeta']= formaPago
        print(formaPago)
        print(str(resp['card_detail']), 'card detail owo')
        if (int(monto) == int(bolsa['precioTotal']) and (status == 'AUTHORIZED')):
            concretarReservaCompleto(id,monto)
            crearBoletaPagoCompleto(formaPago,'WEBPAY',order,monto,id)
            enviarmailBoleta(correoUsuario,monto,nombreDepto,fechaT,formaPago,fechaD,fechaH,nombreDepto,direccionDepto,comunaDepto,regionDepto,digitos)
            del request.session['infoPosibleReserva']
            del request.session['bolsa']
            
            
            
        elif (int(monto) == int(bolsa['abono']) and (status == 'AUTHORIZED')):
            print('es el abono')
            concretarReservaAbono(id,monto)
            crearBoletaPagoAbono(formaPago,'WEBPAY',order,monto,id)
            enviarmailBoleta(correoUsuario,monto,nombreDepto,fechaT,formaPago,fechaD,fechaH,nombreDepto,direccionDepto,comunaDepto,regionDepto,payment_type_code)
            del request.session['infoPosibleReserva']
            del request.session['bolsa']
        else:
            data['mensaje'] = 'hubo un problema al procesar el pago'
    return render(request, 'clientes/ReservaExitosa.html',data)

def detalleParaReservar(request,item):
    usuarioActual = request.session.get("usuario_id")
    if usuarioActual is None:
        return redirect('home')
    data ={
        'depto': datosDepto(item),
        'servicios':datosServicio(),
        'imagenes':traerImagenes(item),
        'fechahoy': datetime.date.today()
    }
    print(data['depto'])
    idUsuario = request.session['usuario_id']
    print(data['imagenes'])
    
    if 'usuario_id' in request.session:
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual

    if request.method == 'POST':
        inicio = request.POST.get('inicio')
        fechaSalida  = request.POST.get('fechaSalida')
        cantHuespedes = request.POST.get('personas')
        #obtengo una lista de los id's de servicio seleccionados en los input 'checkbox'
        idServicio= request.POST.getlist('servicio')
        #aca la cantidad viene con los valores vacios o ceros incluidos, lo que entorpece el calculo con los servicios

        cantidadServicio= request.POST.getlist('cantidad')
        #aqui guardaremos solo los valores que no sean 0 o vacios entonces se complementa con la lista de id servicios
        cantidadServicioLimpio=[]
        for c in cantidadServicio:
            if c != '0':
                cantidadServicioLimpio.append(c)
        # trae valores si en algun dia de los seleccionados ya existe una reserva
        disponibilidad =disponibilidadFecha(item,inicio,fechaSalida) 
        #trae todos los datos del depto segun la id (q se le pasa por url)
        datos = datosDepto(item)
        #aca verificamos si disponibilidad contiene algun valor
        for c in disponibilidad:
            #si la contiene se notifica
            if c[0] != None:
                messages.success(request,f'ya existe una reserva para este departamento entre {c[1]} y {c[2]}, ademas se debe considerar dos dias despues del termino para mantenimiento. por favor, escoge otra fecha')
                break
        else:
            #aquí comienzo a obtener el valor total de los servicios
            precioTotalServicios =0
            iterador=0
            #recorro la lista de id's obtenida anteriormente para obtener el valor de cada servicio 
            for c in idServicio:
                
                #la funcion consultar servicio se le entrega el id del servicio para obtener todos los datos relacionados a este en una tupla
                #y se guarda el valor en la variable 'valor'
                valor = consultarServicio(c)
                
                #se actualiza la variable precio sumandole el valor por cada recorrido y se multiplica por la cantidad de servicios
                precioTotalServicios = precioTotalServicios + (valor[3] * int(cantidadServicioLimpio[iterador]))
                iterador +=1
            #desde el procedimiento almacenado extraigo la cantidad de dias 
            dias = cantDias(inicio,fechaSalida)
            totalDias= extraerValorTupla(dias,0)
            precioNoche = extraerValorTupla(datos[0],5)
            precioTotalDias= totalDias*precioNoche
            #preio total de la reserva
            precioTotalReserva = precioTotalDias+precioTotalServicios
            #el valor del abono
            abono = calcularAbono(precioTotalReserva)
            #valores q se muestran en el front
            data['abono']=abono
            data['TotalReserva']=precioTotalReserva
            pr = True
            data['IDPR']= pr
            crearBolsa(request,totalDias,precioTotalDias,inicio,fechaSalida,item,idServicio,cantidadServicioLimpio,precioTotalServicios,precioTotalReserva,abono,cantHuespedes)
    return render(request, 'clientes/detalleParaReservar.html' ,data)

def solicitarReserva(request):
    bolsa = request.session.get("bolsa")
    if bolsa is None:
        return redirect('home')
    bolsa = request.session['bolsa']
    data = {}
    print(bolsa,1111)
    data['servicios'] = []

    #c es el id de los servicios que selecciono el usuario y se encuentran en la bolsa
    iterador=0
    for c in bolsa['servicios']:
            datosServ = consultarServicio(c)
            cantServ=bolsa['cantidadServiciosLimpio']
            s ={'idServicio':datosServ[0],'nombre':datosServ[1],'precio':datosServ[3], 'cantidad':cantServ[iterador],'total':int(datosServ[3])*int(cantServ[iterador])}
            iterador +=1
            #al diccionario data se le agrega cada lista
            data['servicios'].append(s)

    
    if bolsa['precioTotal'] != 0 and 'usuario_id' in request.session:
        idDepto = bolsa['idDepartamento']
        depto = datosDepto(idDepto)
        print(depto)
        data['depto'] = depto
        data['bolsa']= request.session['bolsa']
        usuarioActual = request.session['usuario']
        data ['usuarioActual']= usuarioActual
    
    

    if request.method == 'POST':
        try:
            valor = request.POST.get('valor') 
            fechaDesde = bolsa['fechaDesde']
            fechaHasta  = bolsa['fechaHasta']
            precioNoche = depto[0][5]
            idDepartamento = bolsa['idDepartamento']
            idUsuario = request.session['usuario_id']
            precioTotalReserva = bolsa['precioTotal']
            
            #Creamos una posible reserva
            crearPosibleReserva(fechaDesde,fechaHasta,precioNoche,idDepartamento,idUsuario,precioTotalReserva)
            #Obtengo el id de la ultima posible reserva que cumpla con el mismo usuario y depto
            idPosibleReserva = obtenerIdPosibleReserva(idUsuario, idDepto)
            idposibleReserva = idPosibleReserva[0][0]
            print(idposibleReserva)

            for c in data['servicios']:
                precioTotalServicios = bolsa['precioTotalServicios']
                crearDetalleServicio(c['total'],c['idServicio'],idposibleReserva,c['cantidad'])
            
            numero = 0
            while True: 
                nombres = request.POST.get(f'huesped{str(numero)}')
                apellido = request.POST.get(f'apellido{str(numero)}')
                rut = request.POST.get(f'rut{str(numero)}')
                if nombres != None:
                    numero +=1
                    print(nombres)
                    print(apellido)
                    print(rut)
                    agregarAcompanantes(nombres, apellido,rut,idposibleReserva)
                else:
                    break

            ##Aca deberiamos crear un numero aleatorio para la orden 
            buy_order = generarNumeroDeOrder()
            ## Versión 3.x del SDK
            tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
            response = tx.create(buy_order, '6jn0gz1jmyfbugwbnwhah8tukauv5a25', valor, 'http://127.0.0.1:8000/ReservaExitosa')
            url = response['url']
            token = response['token']
            #dejamos en una sesion el valor de id y monto para en la vista de confirmar segun lo recibido se ejecuten los SP concretar y boleta segun los parametros anteriores
            infoParaConfirmar(request,idposibleReserva,valor)
            
            data['url']=url
            data['token']=token
            print(data)
        except:
            messages.success(request,"Un error ha ocurrido, por favor revisa tus datos e intentalo nuevamente")
            
        



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

def RReserva(idReserva):
    cursor = connection.cursor()
    params=(idReserva,)
    cursor.execute("{CALL dbo.SP_U_RevisarReserva(%s)}", params)
    resultados = cursor.fetchall()
    return resultados

def servicioExtrasContratados(idReserva,idUsuario):
    cursor = connection.cursor()
    params=(idReserva,idUsuario)
    cursor.execute("{CALL dbo.SP_SE_Contratados(%s,%s)}",params)
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

def crearBolsa(request,dias,precioTotalDias,fechaDesde, fechaHasta,idDepartamento,servicios,cantidadServiciosLimpio,precioTotalServicios,precioTotal,abono,acompañantes):
    consultarBolsa = request.session.get('bolsa')
    if consultarBolsa == None:
        request.session['bolsa']={'fechaDesde':fechaDesde,'dias':dias,'precioTotalDias':precioTotalDias,'fechaHasta':fechaHasta,'idDepartamento':idDepartamento,'servicios':servicios,'cantidadServiciosLimpio':cantidadServiciosLimpio,'precioTotalServicios':precioTotalServicios, 'precioTotal':precioTotal,'abono':abono,'acompañante':acompañantes}
    else:
        del request.session['bolsa']
        crearBolsa(request,dias,precioTotalDias,fechaDesde, fechaHasta,idDepartamento,servicios,cantidadServiciosLimpio,precioTotalServicios,precioTotal,abono,acompañantes)
    
def infoParaConfirmar(request,idPosibleReserva,monto):
    ConsultarinfoPosibleReserva = request.session.get('infoPosibleReserva')
    if ConsultarinfoPosibleReserva == None:
        request.session['infoPosibleReserva']={'idPosibleReserva':idPosibleReserva,'monto':monto}
    else:
        del request.session['infoPosibleReserva']
        infoParaConfirmar(request,idPosibleReserva,monto)

def crearPosibleReserva(fechaDesde, fechaHasta, precioNoche, idDepartamento,idUsuario, precioTotalReserva):
    cursor = connection.cursor()
    params = (fechaDesde, fechaHasta, precioNoche, idDepartamento,idUsuario, precioTotalReserva)
    cursor.execute("{CALL dbo.SP_CrearPosibleReserva(%s,%s,%s,%s,%s,%s)}",params)

def agregarAcompanantes(nombreAcompanante,apellidoAcompanante,identificacion,idReserva):
    cursor = connection.cursor()
    params = (nombreAcompanante,apellidoAcompanante,identificacion,idReserva)
    cursor.execute("{CALL dbo.SP_IngresarAcompanantes(%s,%s,%s,%s)}",params)

def crearDetalleServicio(total,idServicio,idReserva,cantidad):
    cursor = connection.cursor()
    params = (total,idServicio,idReserva,cantidad)
    cursor.execute("{CALL dbo.SP_CrearDetalleServicio(%s,%s,%s,%s)}",params)

def obtenerIdPosibleReserva(idUsuario, idDepto):
    cursor = connection.cursor()
    params=(idUsuario,idDepto)
    cursor.execute("{CALL dbo.SP_ObtenerIdPosibleReserva(%s,%s)}",params)
    resultado = cursor.fetchall()
    return resultado

def traerImagenes(idDepto):
    cursor = connection.cursor()
    params=(idDepto,)
    cursor.execute("{CALL dbo.SP_TraerDescripcionImg(%s)}",params)
    resultados= cursor.fetchall()
    return resultados

def generarNumeroDeOrder():
    conjunto = ['OR-DZ65','OR-CF32','OR-ET79','OR-TK94','OR-WM10']
    lista=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numero   = str(random.randrange(100,900))
    letra = random.choice(lista)
    etiqueta = random.choice(conjunto)
    codigo   = etiqueta+numero+letra
    return codigo

