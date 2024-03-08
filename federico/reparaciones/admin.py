from django.contrib import admin

# Register your models here.
from .models import OrdenDeReparacion, OrdenDeReparacionItem, Reparacion, Supervisor

admin.site.register(OrdenDeReparacion)
admin.site.register(OrdenDeReparacionItem)
admin.site.register(Reparacion)
admin.site.register(Supervisor)
