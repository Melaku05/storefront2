from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view()
def product_list(request):
    queryset =Product.objects.select_related('collection').all() # returns queryset (fix the queryset problem)
     #queryset =Product.objects.all() # returns queryset but we crash our system around 1000 queryset pre request
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
        product = get_object_or_404(Product, pk=id) #checking the id is valid or not and respond with 404 if not
        serializer = ProductSerializer(product)
        return Response(serializer.data)
   
