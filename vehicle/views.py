from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from vehicle.models import Car, Moto, Millage
from vehicle.paginators import VehiclePaginator
from vehicle.permissions import IsOwnerOrStaff
from vehicle.serializers import CarSerializer, MotoSerializer, MillageSerializer, MotoMillageSerializer, \
    MotoCreateSerializer
from vehicle.tasks import check_milage


class CarViewSet(viewsets.ModelViewSet):
    """Cars viewset"""
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated]


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()

    permission_classes = [IsOwnerOrStaff]

class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MillageCreateAPIView(generics.CreateAPIView):
    serializer_class = MillageSerializer

    def perform_create(self, serializer):
        new_milage = serializer.save()
        if new_milage.car :
            check_milage.delay(new_milage.car_id, 'Car')
        else:
            check_milage.delay(new_milage.moto_id, 'Moto')


class MotoMillageAPIView(generics.ListAPIView):
    queryset = Millage.objects.filter(moto__isnull=False)
    serializer_class = MotoMillageSerializer


class MillageListAPIView(generics.ListAPIView):
    serializer_class = MillageSerializer
    queryset = Millage.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('car', 'moto')
    ordering_fields = ('year', )