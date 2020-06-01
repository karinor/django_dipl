from django.contrib.auth import views
from django.urls import path, include
from .views import *

app_name = 'account'

urlpatterns = [
    path('', ProfileDataView.as_view(), name='ProfileData'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('orders/', ProfileOrdersView.as_view(), name='ProfileOrders'),
]