from django.urls import path
from .views import salons

urlpatterns = [
    path('', salons, name='salons'),
]
