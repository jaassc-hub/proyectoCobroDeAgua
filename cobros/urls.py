from django.urls import path
from . import views

app_name = 'cobros'

urlpatterns = [
    path("", views.cobro, name="cobro"),
    path("view/", views.view, name="view"),
    path("pagos/", views.cobro, name="pagos"),
    path("day_payments/", views.day_payments, name="day_payments"),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),


    path("pagos/imprimir_recibo/<int:id>", views.imprimir_recibo, name="imprimir")
]