from dataclasses import dataclass
from django.http import HttpResponse

from multiprocessing.sharedctypes import Value
import random
from django.shortcuts import render, redirect
from django.db import connection
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
import time




def iniciarSesion(request):

    data ={}
    if request.method == 'POST':
        try:
            usuario = request.POST.get('usuario')
            contrasena = request.POST.get('contrasena')
            patron = 'Portafolio'
            user = autenticar(usuario,contrasena,patron)
            request.session['usuario_id'] = user[0]
            request.session['usuario'] = usuario
            return redirect('home')
        except:
            data['mensaje'] = 'Algo salió mal'
    return render(request, 'registration/login.html',data)


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
            idTipoUsuario = 3
            patron = 'Portafolio'
            habilitado= 'Deshabilitado'
            esPasaporte= False
            crearCliente(nombres,apellidos,usuario,correo,contrasena,identificacion,celular,pais,codigoVerificacion,idTipoUsuario,patron,habilitado,esPasaporte)
            success= f"{nombres}, te registraste con exito, verifica el codigo de validacion que se te envió a tu correo"
            enviarEmail(codigoVerificacion,correo)
            return redirect('verificacion')

            
        except:
            success="No pudimos registrarte, revisa tus datos e intentalo nuevamente"
            return HttpResponse(success)

    return render(request,'registration/registro.html',data)

def verificacion(request):
    data = {
    }
    if request.method == 'POST':
        codigoVerificacion = request.POST.get('codigo')
        verificar(codigoVerificacion)
    return render(request, 'registration/Verificacion.html', data)

def generarCodigoVerificacion():
    conjunto = ['FJD6','JNC3','FZE7','QYT9','WMN1']
    lista=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numero   = str(random.randrange(100,900))
    letra = random.choice(lista)
    etiqueta = random.choice(conjunto)
    codigo   = etiqueta+numero+letra
    return codigo

def autenticar(usuario,contra,patron):
    cursor = connection.cursor()
    params = (usuario,contra,patron)
    cursor.execute("{CALL dbo.SP_U_Validar(%s,%s,%s)}",params)
    records = cursor.fetchone()
    return records
    
def verificar(codigo):
    cursor = connection.cursor()
    params = (codigo,)
    cursor.execute("{CALL dbo.SP_VERIFICAR_CODIGO(%s)}",params)

def crearCliente(nombres, apellidos, usuario, correo, contrasena,
                identificacion,celular,pais,codigoVerificacion, 
                idTipoUsuario,patron, habilitada,esPasaporte):

    cursor = connection.cursor()
    params=(nombres, apellidos, usuario, correo, contrasena,identificacion,celular,pais,codigoVerificacion, idTipoUsuario,patron, habilitada,esPasaporte)
    cursor.execute("{CALL dbo.SP_UC_CREAR(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)}",params)
    cursor.close()

def enviarEmail(codigo,correo):
    email = EmailMessage('Valida tu Cuenta en Turismo Real',codigo,settings.EMAIL_HOST_USER,[correo])
    email.send()
