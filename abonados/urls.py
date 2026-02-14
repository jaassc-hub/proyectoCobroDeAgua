
from django.urls import path
from . import views

app_name = 'abonados'

urlpatterns = [
    path("", views.abonados_index, name="view"),
    path("create", views.create_abonado, name="create"),
    path("edit/<int:id>", views.edit_abonado, name="edit"),
    path("delete/<int:id>", views.delete_abonado, name="delete"),
    path("buscar/<str:nombre>", views.buscar_abonado, name="buscar_abonado"),
    path('agregar_abonado_buscador/<str:codigo_pegue>', views.agregar_abonado_buscador, name='agregarAbonadoBuscador'),

]