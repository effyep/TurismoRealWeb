from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('logout' ,views.logout, name ='logout'),
    path('ComoReservar', views.ComoReservar, name='ComoReservar'),
    path('ReservaExitosa', views.reservaExitosa, name = 'reservaExitosa'),
    path('ConfirmarReserva', views.solicitarReserva, name='confirmarReserva'),
    path('DetalleParaReservar/<int:item>', views.detalleParaReservar, name = 'detalleParaReservar'),
    path('Perfil', views.miPerfil, name='perfil')
]