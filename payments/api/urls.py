from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'fees', FeeViewset, basename='fees')
router.register(r'taxes', TaxViewset, basename='taxes')


urlpatterns  = [
    path('',include(router.urls)),
]