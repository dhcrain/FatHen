from django.shortcuts import render
from rest_framework import generics
from review_app.models import FarmersMarket, Vendor
from fm_api.serializers import FarmersMarketSerializer, VendorSerializer
# Create your views here.

class FarmersMarketListAPIView(generics.ListAPIView):
    queryset = FarmersMarket.objects.all()
    serializer_class = FarmersMarketSerializer


class FarmersMarketRetrieveAPIView(generics.RetrieveAPIView):
    queryset = FarmersMarket.objects.all()
    serializer_class = FarmersMarketSerializer


class VendorListAPIView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
