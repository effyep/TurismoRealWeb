from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.db import connection
import random

def registro(request):
    data = {
    }

    if request.method == 'POST':
        try:
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            usuario = request.POST.get('usuario')
            correo = request.POST.get('email')
            contrasena=request.POST.get('contraseña')
            identificacion = request.POST.get('identificacion')
            celular = request.POST.get('celular')
            pais = request.POST.get('pais')
            codigoVerificacion = generarCodigoVerificacion()
            idTipoUsuario = 1
            patron = 'Portafolio'
            habilitado= False
            esPasaporte= False
            crearCliente(nombres,apellidos,usuario,correo,contrasena,identificacion,celular,pais,codigoVerificacion,idTipoUsuario,patron,habilitado,esPasaporte)
            data ['mensaje']= f"{nombres, apellidos}, te registraste con exito, verifica el codigo de validacion que se te envió a tu correo"
        except:
            data ['mensaje'] = "Algo salio mal"


    return render(request,'registration/registro.html',data)

def generarCodigoVerificacion():
    conjunto = ['FJD6','JNC3','FZE7','QYT9','WMN1']
    lista=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numero   = str(random.randrange(100,900))
    letra = random.choice(lista)
    etiqueta = random.choice(conjunto)
    codigo   = etiqueta+numero+letra
    return codigo

def crearCliente(nombres, apellidos, usuario, correo, contrasena,
                identificacion,celular,pais,codigoVerificacion, 
                idTipoUsuario,patron, habilitada,esPasaporte):

    cursor = connection.cursor()
    params=(nombres, apellidos, usuario, correo, contrasena,identificacion,celular,pais,codigoVerificacion, idTipoUsuario,patron, habilitada,esPasaporte)
    cursor.execute("{CALL dbo.SP_UC_CREAR(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)}",params)
    
