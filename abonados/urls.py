
from django.urls import path
from . import views

urlpatterns = [
    path("", views.abonados_index, name="abonados"),
    path("create", views.crear_abonado, name="create_abonado"),
    path("buscar/<str:nombre>", views.buscar_abonado, name="buscar_abonado"),
    path('agregar_abonado_buscador/<str:codigo_pegue>', views.agregar_abonado_buscador, name='agregarAbonadoBuscador'),

]