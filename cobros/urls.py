from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cobro/", views.cobro, name="cobro"),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),

    path("pagos/", views.pagos_index, name="pagos"),
]