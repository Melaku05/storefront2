from unicodedata import lookup
from django.urls import path
#from rest_framework.routers import DefaultRouter #SimpleRouter
from rest_framework_nested import routers

from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')

review_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
review_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')
# app_name = 'store'

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register(r'items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls)),
    path('', include(carts_router.urls))
]   
