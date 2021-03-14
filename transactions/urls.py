from rest_framework import routers
from .views import TransactionView
from django.conf.urls import include, url

router = routers.SimpleRouter()
router.register(r'transactions', TransactionView, basename='TransactionModel')

urlpatterns = [
    url(r'^', include(router.urls)),]