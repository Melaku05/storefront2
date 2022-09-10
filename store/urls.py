from django.urls import path
from rest_framework.routers import DefaultRouter #SimpleRouter

from . import views

router = DefaultRouter()
router.register('products', views.ProductViewListSet)
router.register('collections', views.CollectionViewListSet)
urlpatterns = router.urls
