from rest_framework import serializers
from reparaciones.models import *
from tablamadre.models import *


class ReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reparacion
        fields = '__all__'


class OrdenReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeReparacion
        fields = '__all__'


class OrdenReparacionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeReparacionItem
        fields = '__all__'


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = '__all__'


class MecanicoEncargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MecanicoEncargado
        fields = '__all__'


class ParteDiarioMecanicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParteDiarioMecanicos
        fields = '__all__'


class InternoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internos
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialService
        fields = '__all__'


class NovedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedades
        fields = '__all__'


class UPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadesdeProduccion
        fields = '__all__'


class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choferes
        fields = '__all__'


class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operadores
        fields = '__all__'


class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = '__all__'


class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = '__all__'


class UrgenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urgencia
        fields = '__all__'


class FiltroInternosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiltrosInternos
        fields = '__all__'


class NeumaticoInternosSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeumaticosInternos
        fields = '__all__'


class TanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tanque
        fields = '__all__'


class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = '__all__'


class RepostajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repostaje
        fields = '__all__'


class TanqueAceiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tanque
        fields = '__all__'


class ConsumoAceiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = '__all__'


class RepostajeAceiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repostaje
        fields = '__all__'

