from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from store import serializers
# if our views class have not logic, we can smplify further like this:

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all() # returns queryset (fix the queryset problem)
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer

class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')) 
    serializer_class = CollectionSerializer

class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'message': 'You can not delete this collection'}, status=status.HTTP_400_BAD_REQUEST) 
        collection.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



