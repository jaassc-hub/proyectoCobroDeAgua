
from django.urls import path
from . import views

app_name = 'abonados'

urlpatterns = [
    path("", views.abonados_index, name="abonados"),
    path("create", views.crear_abonado, name="create"),
    path("buscar/<str:nombre>", views.buscar_abonado, name="buscar_abonado"),
    path('agregar_abonado_buscador/<str:codigo_pegue>', views.agregar_abonado_buscador, name='agregarAbonadoBuscador'),

]