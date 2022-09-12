from rest_framework import serializers
from .models import Product, Collection, Review

class ProductSerializer(serializers.ModelSerializer):
    '''
    ProductSerializer class inherit ModelSerializer class from rest_framework, Modelserializer is save method ,to create or update our product model
    '''
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'inventory', 'last_update', 'collection']
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    

class CollectionSerializer(serializers.ModelSerializer):
    '''
    CollectionSerializer class inherit ModelSerializer class from rest_framework, Modelserializer is save method ,to create or update our collection model
    '''
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    '''
    ReviewSerializer class inherit ModelSerializer class from rest_framework, Modelserializer is save method ,to create or update our review model
    '''
    class Meta:
        model = Review
        fields = ['id', 'product', 'name','description', 'date']
    
    
    