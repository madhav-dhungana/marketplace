from rest_framework import exceptions, status,viewsets
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import FeeModel,TransactionModel,TaxModel
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from mainproject.pagination import CustomPagination
from user.api.permissions import IsBatuwaAdminOnly

class FeeViewset(viewsets.ModelViewSet):
    queryset = FeeModel.objects.all()
    serializer_class = FeeSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    permission_classes  =[IsBatuwaAdminOnly]
    search_fields = ("name",)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.id
        self.perform_destroy(instance)
        return Response( {'type':'delete','id':pk}, status=status.HTTP_200_OK)

class TaxViewset(viewsets.ModelViewSet):
    queryset = TaxModel.objects.all()
    serializer_class = TaxSerializer
    permission_classes  =[IsBatuwaAdminOnly]
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    search_fields = ("name",)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.id
        self.perform_destroy(instance)
        return Response( {'type':'delete','id':pk}, status=status.HTTP_200_OK)

class TransactionViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    search_fields = ("name",)
    permission_classes=[IsAuthenticated]