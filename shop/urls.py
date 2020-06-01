from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', cartView.as_view(), name='CartDetails'),
    path('order/', orderView.as_view(), name='OrderDetails'),
]