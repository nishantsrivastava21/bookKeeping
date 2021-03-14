from rest_framework import routers
from .views import ContactView
from django.conf.urls import include, url

router = routers.SimpleRouter()
router.register(r'contacts', ContactView, basename='ContactModel')

urlpatterns = [
    url(r'^', include(router.urls)),]