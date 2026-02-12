from django.db import models
from django.contrib.auth.models import User
from pegues.models import Pegue


class Pago(models.Model):
    pegue = models.ForeignKey(Pegue, on_delete=models.CASCADE, related_name="pagos")
    anio = models.IntegerField()
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=20, choices=[('EFEC', 'EFEC'), ('TRNF', 'TRNF')],default='EFEC')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('pegue', 'anio', 'mes')
        ordering = ['-anio', '-mes']
    

    def __str__(self):
        return f"{self.pegue} - {self.mes}/{self.anio} - {self.monto} L"