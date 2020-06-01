from django.contrib.auth.models import User
from account.models import Profile
from shop.models import Order, OrderedProducts
from django.shortcuts import render


class PrintableOrders:
    
    def __init__(self, orders):
        self.orders = {}
        for order in orders:
            products = []
            for ordered_product in OrderedProducts.objects.filter(order=order.id):
                products.append(
                    {
                        'product': ordered_product.product,
                        'count': ordered_product.count
                    }
                )
                self.orders[order.id] = {
                    'id': order.id,
                    'status': order.status,
                    'date': order.date,
                    'products': products,
                    'total': order.payment.total if order.payment.total is not None else 1
                }
    
    def __iter__(self):
        for order in self.orders:
            yield self.orders[order]