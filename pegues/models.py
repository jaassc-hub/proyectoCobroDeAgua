from django.db import models

from abonados.models import Abonado
from barrios.models import Barrio
from servicios.models import LineaDistribucion, Servicio

# Create your models here.
class Pegue(models.Model):
    codigo_pegue = models.CharField(max_length=6, unique=True)
    abonado = models.ForeignKey(Abonado, on_delete=models.CASCADE, related_name="pegues")
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT, related_name="abonados")
    linea_distribucion = models.ForeignKey(LineaDistribucion,on_delete=models.PROTECT, related_name="abonados", blank=True, null=True)
    estado = models.CharField(choices=[('HAB', 'Habilitada'), ('INH', 'Inhabilitada'), ('CRT', 'Cortada')], max_length=10, default='HAB')
    tipo = models.CharField(choices=[('VIV', 'Vivienda'), ('COR', 'Corral'), ('SOL', 'Solar'), ('COM', 'Comercio')], max_length=10, default='VIV')
    servicios = models.ManyToManyField(Servicio, related_name="abonados")
    fecha_instalacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pegue: {self.abonado.nombre} - {self.barrio.nombre} - {self.linea_distribucion.codigo}"
    

    @property
    def tarifa_mensual(self):
        """Suma de todos los servicios activos asignados al pegue"""
        return sum(servicio.monto for servicio in self.servicios.filter(activo=True))
    
