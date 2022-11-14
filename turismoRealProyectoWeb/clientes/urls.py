from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('logout' ,views.logout, name ='logout'),
    path('ComoReservar', views.ComoReservar, name='ComoReservar'),
    path('ReservaExitosa', views.reservaExitosa, name = 'reservaExitosa'),
    path('ConfirmarReserva/<int:item>', views.solicitarReserva, name='confirmarReserva'),
    path('DetalleParaReservar/<int:item>', views.detalleParaReservar, name = 'detalleParaReservar'),
    path('RevisarReserva/<int:item>', views.revisarReserva, name = 'revisarReserva'),
    path('Perfil', views.miPerfil, name='perfil'),
    path('WebPaySimilacion', views.webpay, name='webpay'),
    path('ListarUsuarios',views.listarUsuarios, name = 'usuarios')
]