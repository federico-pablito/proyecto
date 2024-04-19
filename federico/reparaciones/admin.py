from django.contrib import admin

# Register your models here.
from .models import OrdenDeReparacion, OrdenDeReparacionItem, Reparacion, Supervisor, Taller, MecanicoEncargado, ParteDiarioMecanicos

admin.site.register(OrdenDeReparacion)
admin.site.register(OrdenDeReparacionItem)
admin.site.register(Reparacion)
admin.site.register(Supervisor)
admin.site.register(Taller)
admin.site.register(MecanicoEncargado)
admin.site.register(ParteDiarioMecanicos)
