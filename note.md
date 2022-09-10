
generic views override to method
get queryset
get serilaizer context


```
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all() # returns queryset (fix the queryset problem)
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

 # if our views class have not logic, we can smplify further like this:

class ProductList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all() # returns queryset (fix the queryset problem)
    
    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
```