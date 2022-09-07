from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from store import serializers

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':

        queryset =Product.objects.select_related('collection').all() # returns queryset (fix the queryset problem)
         #queryset =Product.objects.all() # returns queryset but we crash our system around 1000 queryset pre request
        serializer = ProductSerializer(queryset, many=True ,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id) #checking the id is valid or not and respond with 404 if not
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        collection=Collection.objects.annotate(products_count=Count('products'))
        serializer= CollectionSerializer(collection, many=True)
        return Response(serializer.data)
    elif request.method == 'POST': 
        serializer = CollectionSerializer(data=request.data) #Deserializes data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])  
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if collection.products_count > 0:
            return Response({'message': 'You can not delete this collection'}, status=status.HTTP_400_BAD_REQUEST) 
        collection.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

