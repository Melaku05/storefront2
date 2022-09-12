from django.urls import path
#from rest_framework.routers import DefaultRouter #SimpleRouter
from rest_framework_nested import routers

from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
review_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
review_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')
app_name = 'store'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls)),
]
