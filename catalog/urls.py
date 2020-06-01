from django.urls import path, include
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('compare/', CompareTemplateView.as_view(), name='CompareDetails'),
    path('favorites/', FavoritesTemplateView.as_view(), name='FavoritesDetails'),
    path('', CategoryListTemplateView.as_view(), name='CategoryList'),
    path('products/<str:slug>', ProductDetailView.as_view(), name='ProductDetails'),
    path('<str:slug>/', CategoryDetailView.as_view(), name='CategoryDetails'),
]
