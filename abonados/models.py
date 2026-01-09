from django.db import models

# Create your models here.
class Abonado(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=13, unique=True, blank=True, null=False, default="")
    telefono = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.nombre


