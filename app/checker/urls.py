from django.urls import path
from .views import index, certificate

urlpatterns = [
    path('', index),
    path('certificate/', certificate),
]
