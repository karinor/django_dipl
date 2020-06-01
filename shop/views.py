from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, View
from django.http import JsonResponse
from django.template.loader import get_template
from catalog.modules.post_actions import PostActions, OrderPost
from catalog.models import Product
from .cart import Cart, CartAuth
from django.urls import reverse
from .forms import OrderForm
from account.models import Profile
from django.contrib.auth.models import User
# Create your views here.

class cartView(PostActions, View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = CartAuth(request)
        else:
            cart = Cart(request)
        context = dict()
        context["products"] = cart.get()
        return render(request, self.template_name, context)


class orderView(OrderPost, View):
    template_name = 'order.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = CartAuth(request)
        else:
            cart = Cart(request)
        print(len(cart))
        if len(cart) < 1:
            return redirect(reverse('CartDetails'))
        else:
            context = dict()
            context["cart"] = cart
            print(type(cart))
            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                auto_fill = {
                    'fullname': request.user.last_name,
                    'email': request.user.username,
                    'phone': profile.phone
                }
            context['form'] = OrderForm(initial=auto_fill)
            return render(request, self.template_name, context)
    
    
        
