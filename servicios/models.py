from django.db import models

# Create your models here.
class Servicio(models.Model):
    nombre = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (L {self.monto})"
    

class LineaDistribucion(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    numero_valvulas = models.PositiveIntegerField()

    def __str__(self):
        return f"Línea {self.codigo} ({self.numero_valvulas} válvulas)"

