from django.contrib import admin
from django.contrib.auth.models import Permission, User
from .models import (Choferes, Internos, Services, UnidadesdeProduccion,
                     Novedades, DisponibilidadEquipos, TipoActividad, MecanicosEncargados, AlquilerEquipos,
                     CertificadosEquiposAlquilados, HistorialService, Talleres, Urgencia,
                     TipoVehiculo, FiltrosInternos, NeumaticosInternos, Tanque, Consumo,
                     Repostaje, TanqueAceite, ConsumoAceite, RepostajeAceite)


# Register your models here.
admin.site.register(Internos)
admin.site.register(Services)
admin.site.register(UnidadesdeProduccion)
admin.site.register(Novedades)
admin.site.register(Choferes)
admin.site.register(DisponibilidadEquipos)
admin.site.register(TipoActividad)
admin.site.register(Talleres)
admin.site.register(MecanicosEncargados)
admin.site.register(AlquilerEquipos)
admin.site.register(CertificadosEquiposAlquilados)
admin.site.register(HistorialService)

admin.site.register(TipoVehiculo)
admin.site.register(Urgencia)
admin.site.register(FiltrosInternos)
admin.site.register(NeumaticosInternos)
admin.site.register(Tanque)
admin.site.register(Consumo)
admin.site.register(Repostaje)
admin.site.register(Permission)
admin.site.register(TanqueAceite)
admin.site.register(ConsumoAceite)
admin.site.register(RepostajeAceite)
