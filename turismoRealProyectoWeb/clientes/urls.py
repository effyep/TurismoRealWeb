from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('Busqueda', views.busqueda, name='busqueda'),
    path('home', views.home, name = 'home'),
    path('logout' ,views.logout, name ='logout'),
    path('ComoReservar', views.ComoReservar, name='ComoReservar'),
    path('ReservaExitosa', views.reservaExitosa, name = 'reservaExitosa'),
    path('SolicitarReserva', views.solicitarReserva, name='solicitarReserva'),
    path('ResultadosBusqueda', views.resultadosBusqueda, name= 'resultadosBusqueda')
]