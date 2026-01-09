
from django.urls import path
from . import views

urlpatterns = [
    path("", views.abonados_index, name="abonados"),
    path("crear_abonado", views.crear_abonado, name="crear_abonado"),
    path("buscar/<str:nombre>", views.buscar_abonado, name="buscar_abonado"),
    path('agregar_abonado_buscador/<str:codigo_pegue>', views.agregar_abonado_buscador, name='agregarAbonadoBuscador'),

]