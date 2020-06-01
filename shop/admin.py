from django.contrib import admin
from .models import Order, OrderedProducts
from account.models import Cart

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    sortable_by = ['user']
    list_display = [
        'product', 'count', 'user',
    ]

admin.site.register(Order)
admin.site.register(OrderedProducts)
admin.site.register(Cart, CartAdmin)
