from django.urls import path
#from rest_framework.routers import DefaultRouter #SimpleRouter
from rest_framework_nested import routers

from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('products', views.ProductViewListSet)
router.register('collections', views.CollectionViewListSet)
router.register('reviews', views.ReviewViewListSet)
review_router = routers.NestedSimpleRouter(router, r'products', lookup='products')
review_router.register(r'reviews', views.ReviewViewListSet, basename='product-reviews')
app_name = 'store'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls)),
]
