from django.contrib import admin
from .models import (Choferes, Consumos, TablaMadre, Internos, Services, UnidadesdeProduccion, Reparaciones, Logistica,
                     PartesDiarios, Novedades, DisponibilidadEquipos, TipoActividad, MecanicosEncargados, AlquilerEquipos,
                     CertificadosEquiposAlquilados, HistorialService, Talleres)


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
admin.site.register(DisponibilidadEquipos)
admin.site.register(TipoActividad)
admin.site.register(MecanicosEncargados)
admin.site.register(Talleres)
admin.site.register(AlquilerEquipos)
admin.site.register(CertificadosEquiposAlquilados)
admin.site.register(HistorialService)
