from django.urls import path
from . import views

app_name = 'pegues'

urlpatterns = [
    path("", views.pegues_index, name="views"),
    path("obtener_informacion_pegue/<str:codigo_pegue>/", views.obtener_informacion_pegue, name="obtener_informacion_pegue"),
    path("listado_pegues/", views.view, name="view"),
    path("create_pegue/", views.create, name="create"),
    
    path("pegues_mora/", views.pegues_mora, name="pegues-mora"),
    path("pegues_inhabilitados/", views.pegues_inhabilitados, name="pegues-inhabilitados"),
    path("pegues_corrales/", views.pegues_corrales, name="pegues-corrales"),
    path("pegues_solares/", views.pegues_solares, name="pegues-solares"),
    path("pegues_vendidos/", views.pegues_vendidos, name="pegues-vendidos"),
    path("pegues_futuro/", views.pegues_futuro, name="pegues-futuro"),

]