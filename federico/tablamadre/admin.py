from django.contrib import admin
from .models import Choferes, Consumos, TablaMadre, Internos, Services, UnidadesdeProduccion, Reparaciones, Logistica, PartesDiarios, Novedades


# Register your models here.
admin.site.register(Internos)
admin.site.register(Choferes)
admin.site.register(Consumos)
admin.site.register(TablaMadre)
admin.site.register(Services)
admin.site.register(UnidadesdeProduccion)
admin.site.register(Reparaciones)
admin.site.register(Logistica)
admin.site.register(PartesDiarios)
admin.site.register(Novedades)

