from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import permissions
from reparaciones.models import Reparacion, OrdenDeReparacion
from tablamadre.models import *
from .serializers import *


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ReparacionList(APIView):

    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        # Use this method to filter the queryset based on the incoming request
        queryset = Reparacion.objects.all()
        interno = self.request.query_params.get('interno', None)
        taller = self.request.query_params.get('taller', None)
        supervisor = self.request.query_params.get('supervisor', None)
        mecanico_encargado = self.request.query_params.get('mecanico_encargado', None)
        falla_general = self.request.query_params.get('falla_general', None)
        estado_reparacion = self.request.query_params.get('estado_reparacion', None)
        estado_equipo = self.request.query_params.get('estado_equipo', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__contains=interno)
        if taller is not None:
            queryset = queryset.filter(taller__nombre__icontains=taller)
        if supervisor is not None:
            queryset = queryset.filter(supervisor__nombre__icontains=supervisor)
        if mecanico_encargado is not None:
            queryset = queryset.filter(mecanico_encargado__codigo__icontains=mecanico_encargado)

        if falla_general is not None:
            queryset = queryset.filter(falla_general__icontains=falla_general)

        if estado_reparacion is not None:
            queryset = queryset.filter(estado_reparacion__icontains=estado_reparacion)

        if estado_equipo is not None:
            queryset = queryset.filter(estado_equipo__icontains=estado_equipo)

        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ReparacionSerializer(queryset, many=True)
        return Response(serializer.data)


class OrdenReparacionList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = OrdenDeReparacion.objects.all()
        up = self.request.query_params.get('up', None)
        if up is not None:
            queryset = queryset.filter(up__unidadproduccion__icontains=up)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = OrdenReparacionSerializer(queryset, many=True)
        return Response(serializer.data)


class OrdenReparacionItemList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = OrdenDeReparacionItem.objects.all()
        almacen = self.request.query_params.get('almacen', None)
        if almacen is not None:
            queryset = queryset.filter(almacen__icontains=almacen)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = OrdenReparacionItemSerializer(queryset, many=True)
        return Response(serializer.data)


class InternosList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Internos.objects.all()

        interno = self.request.query_params.get('interno', None)
        marca = self.request.query_params.get('marca', None)
        modelo = self.request.query_params.get('modelo', None)
        patente = self.request.query_params.get('patente', None)
        anio = self.request.query_params.get('anio', None)
        aseguradora = self.request.query_params.get('aseguradora', None)
        propietario = self.request.query_params.get('propietario', None)
        tipovehiculo = self.request.query_params.get('tipovehiculo', None)
        up = self.request.query_params.get('up', None)
        alquilado = self.request.query_params.get('alquilado', None)

        if interno is not None:
            queryset = queryset.filter(interno__icontains=interno)
        if marca is not None:
            queryset = queryset.filter(marca__icontains=marca)
        if modelo is not None:
            queryset = queryset.filter(modelo__icontains=modelo)
        if patente is not None:
            queryset = queryset.filter(patente__icontains=patente)
        if anio is not None:
            queryset = queryset.filter(anio__icontains=anio)
        if aseguradora is not None:
            queryset = queryset.filter(aseguradora__icontains=aseguradora)
        if propietario is not None:
            queryset = queryset.filter(propietario__icontains=propietario)
        if tipovehiculo is not None:
            queryset = queryset.filter(tipovehiculo__tipo__icontains=tipovehiculo)
        if up is not None:
            queryset = queryset.filter(up__icontains=up)
        if alquilado is not None:
            alquilado_value = alquilado.lower() in ['true', '1', 't']
            queryset = queryset.filter(alquilado=alquilado_value)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = InternoSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = HistorialService.objects.all()
        interno = self.request.query_params.get('interno', None)
        operativo = self.request.query_params.get('operativo', None)
        necesidadservice = self.request.query_params.get('necesidad_service', None)
        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if operativo is not None:
            queryset = queryset.filter(operativo=operativo)
        if necesidadservice is not None:
            queryset = queryset.filter(necesidadservice__icontains=necesidadservice)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)


class NovedadList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Novedades.objects.all()
        interno = self.request.query_params.get('interno', None)
        reparado = self.request.query_params.get('reparado', None)
        tipo_falla = self.request.query_params.get('tipo_falla', None)
        chofer = self.request.query_params.get('chofer', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if reparado is not None:
            reparado_value = reparado.lower() in ['true', '1', 't']
            queryset = queryset.filter(reparado=reparado_value)
        if tipo_falla is not None:
            queryset = queryset.filter(tipo_falla__icontains=tipo_falla)
        if chofer is not None:
            queryset = queryset.filter(chofer__icontains=chofer)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = NovedadSerializer(queryset, many=True)
        return Response(serializer.data)


class UPList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = UnidadesdeProduccion.objects.all()
        unidadproduccion = self.request.query_params.get('up', None)
        ubicacion = self.request.query_params.get('ubicacion', None)

        if unidadproduccion is not None:
            queryset = queryset.filter(unidadproduccion__icontains=unidadproduccion)
        if ubicacion is not None:
            queryset = queryset.filter(ubicacion__icontains=ubicacion)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = UPSerializer(queryset, many=True)
        return Response(serializer.data)


class ChoferList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Choferes.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        apellido = self.request.query_params.get('apellido', None)
        dni = self.request.query_params.get('dni', None)
        interno = self.request.query_params.get('interno', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido is not None:
            queryset = queryset.filter(apellido__icontains=apellido)
        if dni is not None:
            queryset = queryset.filter(dni__icontains=dni)
        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ChoferSerializer(queryset, many=True)
        return Response(serializer.data)


class OperadorList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Operadores.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        apellido = self.request.query_params.get('apellido', None)
        dni = self.request.query_params.get('dni', None)
        interno = self.request.query_params.get('interno', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido is not None:
            queryset = queryset.filter(apellido__icontains=apellido)
        if dni is not None:
            queryset = queryset.filter(dni__icontains=dni)
        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = OperadorSerializer(queryset, many=True)
        return Response(serializer.data)


class TipoActividadList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = TipoActividad.objects.all()
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = TipoActividadSerializer(queryset, many=True)
        return Response(serializer.data)


class TipoVehiculoList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = TipoVehiculo.objects.all()
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = TipoVehiculoSerializer(queryset, many=True)
        return Response(serializer.data)


class UrgenciaList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Urgencia.objects.all()
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = UrgenciaSerializer(queryset, many=True)
        return Response(serializer.data)


class FiltroInternosList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = FiltrosInternos.objects.all()
        interno = self.request.query_params.get('interno', None)
        marca = self.request.query_params.get('marca', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if marca is not None:
            queryset = queryset.filter(marca__icontains=marca)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = FiltroInternosSerializer(queryset, many=True)
        return Response(serializer.data)


class NeumaticoInternosList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = NeumaticosInternos.objects.all()
        interno = self.request.query_params.get('interno', None)
        marca = self.request.query_params.get('marca', None)
        medida = self.request.query_params.get('medida', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if marca is not None:
            queryset = queryset.filter(marca__icontains=marca)
        if medida is not None:
            queryset = queryset.filter(medida__icontains=medida)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = NeumaticoInternosSerializer(queryset, many=True)
        return Response(serializer.data)


class TanqueList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Tanque.objects.all()
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = TanqueSerializer(queryset, many=True)
        return Response(serializer.data)


class ConsumoList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Consumo.objects.all()
        interno = self.request.query_params.get('interno', None)
        tanque = self.request.query_params.get('tanque', None)
        chofer = self.request.query_params.get('chofer_apellido', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if tanque is not None:
            queryset = queryset.filter(tanque__nombre__icontains=tanque)
        if chofer is not None:
            queryset = queryset.filter(chofer__apellido__icontains=chofer)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ConsumoSerializer(queryset, many=True)
        return Response(serializer.data)


class RepostajeList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Repostaje.objects.all()
        proveedor = self.request.query_params.get('proveedor', None)
        tanque = self.request.query_params.get('tanque', None)

        if proveedor is not None:
            queryset = queryset.filter(proveedor__icontains=proveedor)
        if tanque is not None:
            queryset = queryset.filter(tanque__nombre__icontains=tanque)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = RepostajeSerializer(queryset, many=True)
        return Response(serializer.data)


class TanqueAceiteList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = TanqueAceite.objects.all()
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = TanqueAceiteSerializer(queryset, many=True)
        return Response(serializer.data)


class ConsumoAceiteList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = ConsumoAceite.objects.all()
        interno = self.request.query_params.get('interno', None)
        tanque_aceite = self.request.query_params.get('tanque', None)
        chofer = self.request.query_params.get('chofer_apellido', None)

        if interno is not None:
            queryset = queryset.filter(interno__interno__icontains=interno)
        if tanque_aceite is not None:
            queryset = queryset.filter(tanque_aceite__nombre__icontains=tanque_aceite)
        if chofer is not None:
            queryset = queryset.filter(chofer__apellido__icontains=chofer)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ConsumoAceiteSerializer(queryset, many=True)
        return Response(serializer.data)


class RepostajeAceiteList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = RepostajeAceite.objects.all()
        proveedor = self.request.query_params.get('proveedor', None)
        reservorio_aceite = self.request.query_params.get('tanque', None)

        if proveedor is not None:
            queryset = queryset.filter(proveedor__icontains=proveedor)
        if reservorio_aceite is not None:
            queryset = queryset.filter(reservorio_aceite__nombre__icontains=reservorio_aceite)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = RepostajeAceiteSerializer(queryset, many=True)
        return Response(serializer.data)


class SupervisorList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Supervisor.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        apellido = self.request.query_params.get('apellido', None)
        puesto = self.request.query_params.get('puesto', None)
        especialidad = self.request.query_params.get('especialidad', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido is not None:
            queryset = queryset.filter(apellido__icontains=apellido)
        if puesto is not None:
            queryset = queryset.filter(puesto__icontains=puesto)
        if especialidad is not None:
            queryset = queryset.filter(especialidad__icontains=especialidad)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = SupervisorSerializer(queryset, many=True)
        return Response(serializer.data)


class TallerList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Taller.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        ubicacion = self.request.query_params.get('ubicacion', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if ubicacion is not None:
            queryset = queryset.filter(ubicacion__icontains=ubicacion)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = TallerSerializer(queryset, many=True)
        return Response(serializer.data)


class MecanicoEncargadoList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = MecanicoEncargado.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        apellido = self.request.query_params.get('apellido', None)
        taller = self.request.query_params.get('taller', None)
        codigo = self.request.query_params.get('codigo', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido is not None:
            queryset = queryset.filter(apellido__icontains=apellido)
        if taller is not None:
            queryset = queryset.filter(taller__nombre__icontains=taller)
        if codigo is not None:
            queryset = queryset.filter(codigo__icontains=codigo)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = MecanicoEncargadoSerializer(queryset, many=True)
        return Response(serializer.data)


class ParteDiarioMecanicosList(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = ParteDiarioMecanicos.objects.all()
        mecanico = self.request.query_params.get('mecanico', None)
        actividad = self.request.query_params.get('actividad', None)

        if mecanico is not None:
            queryset = queryset.filter(mecanico__codigo__icontains=mecanico)
        if actividad is not None:
            queryset = queryset.filter(actividad__icontains=actividad)
        return queryset

    def get(self, request, format=None):
        # Get query params
        queryset = self.get_queryset()
        serializer = ParteDiarioMecanicosSerializer(queryset, many=True)
        return Response(serializer.data)
