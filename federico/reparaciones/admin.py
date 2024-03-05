from django.contrib import admin

# Register your models here.
from .models import OrdenDeReparacion, OrdenDeReparacionItem

admin.site.register(OrdenDeReparacion)
admin.site.register(OrdenDeReparacionItem)
