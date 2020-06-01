from django.urls import path, include
from .views import *

app_name = 'pages'

urlpatterns = [
    path("", IndexView.as_view(), name="IndexPage"),
    path("clients", ClientamView.as_view(), name="ClientamPage"),
    path("contacts", ContactsView.as_view(), name="ContactsPage"),
    path("brands", BrandsView.as_view(), name="BrandsPage"),
    
]
