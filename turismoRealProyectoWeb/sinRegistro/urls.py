from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('Registrarse',views.registro, name="Registrarse"),
    path('IniciarSesion', views.iniciarSesion, name="iniciarSesion"),
    path('Verificar', views.verificacion, name ="verificacion")
]

