from django.urls import path
from . import views

urlpatterns = [
    path('Registrarse',views.registro, name="registro")
]

