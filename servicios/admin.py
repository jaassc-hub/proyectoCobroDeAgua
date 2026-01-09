from django.contrib import admin

from servicios.models import LineaDistribucion, Servicio

# Register your models here.
admin.site.register(Servicio)
admin.site.register(LineaDistribucion)
