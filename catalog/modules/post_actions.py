from django.views.generic.detail import SingleObjectMixin
from catalog.compare import Compare, CompareAuth
from catalog.favorites import Favorites, FavoritesAuth
from shop.cart import Cart, CartAuth
from catalog.models import Product
from django.http import JsonResponse
from django.template.loader import get_template
from shop.models import Order, Entity, Delivery, Payment, OrderedProducts
from shop.forms import OrderForm
from django.contrib.auth.models import User
from account.models import Profile
from django.shortcuts import redirect
from django.urls import reverse


class PostActions(SingleObjectMixin):
    def post(self, request, *args, **kwargs):
        action_type = request.POST.get('action')
        if action_type is not None:
            data = dict()
            if action_type == 'compare':
                add_pk = request.POST.get('add', None)
                remove_pk = request.POST.get('remove', None)
                if add_pk is not None and add_pk.isdigit():
                    if request.user.is_authenticated:
                        compare = CompareAuth(request)
                    else:
                        compare = Compare(request)
                    compare.add(add_pk)
                    data['compare_count'] = len(compare)
                elif remove_pk is not None and remove_pk.isdigit():
                    if request.user.is_authenticated:
                        compare = CompareAuth(request)
                    else:
                        compare = Compare(request)
                    compare.remove(remove_pk)
                    context = dict()
                    compare_len = len(compare)
                    context['compare_count'] = compare_len
                    context['id'] = remove_pk
                    if compare_len == 0:
                        return JsonResponse({
                            'empty': get_template('compare_empty.html').render(context=None, request=request), 
                            'compare_count': compare_len,
                        })
                    else:
                        return JsonResponse(context)
            elif action_type == 'favorites':
                add_pk = request.POST.get('add', None)
                remove_pk = request.POST.get('remove', None)
                if add_pk is not None and add_pk.isdigit():
                    if request.user.is_authenticated:
                        favorites = FavoritesAuth(request)
                    else:
                        favorites = Favorites(request)
                    favorites.add(add_pk)
                    data['favorites_count'] = len(favorites)
                elif remove_pk is not None and remove_pk.isdigit():
                    if request.user.is_authenticated:
                        favorites = FavoritesAuth(request)
                    else:
                        favorites = Favorites(request)
                    favorites.remove(remove_pk)
                    context = dict()
                    favorites_len = len(favorites)
                    context['favorites_count'] = favorites_len
                    context['id'] = remove_pk
                    if favorites_len == 0:
                        return JsonResponse({
                            'empty': get_template('favorites_empty.html').render(context=None, request=request), 
                            'favorites_count': favorites_len,
                        })
                    else:
                        return JsonResponse(context)
            elif action_type == 'cart':
                add_pk = request.POST.get('add', None)
                count = request.POST.get('count', None)
                update_pk = request.POST.get('update', None)
                remove_pk = request.POST.get('remove', None)
                if add_pk is not None and add_pk.isdigit():
                    if request.user.is_authenticated:
                        cart = CartAuth(request)
                    else:
                        cart = Cart(request)
                    if count is not None and count.isdigit():
                        cart.add(add_pk, count)
                    else:
                        cart.add(add_pk)
                    data['cart_count'] = len(cart)
                elif remove_pk is not None and remove_pk.isdigit():
                    if request.user.is_authenticated:
                        cart = CartAuth(request)
                    else:
                        cart = Cart(request)
                    cart.remove(remove_pk)
                    context = dict()
                    cart_len = len(cart)
                    context['cart_count'] = cart_len
                    context['id'] = remove_pk
                    if cart_len == 0:
                        return JsonResponse({
                            'empty': get_template('cart_empty.html').render(context=None, request=request), 
                            'cart_count': cart_len,
                        })
                    else:
                        return JsonResponse(context)
                elif update_pk is not None and update_pk.isdigit():
                    count = request.POST.get('count', None)
                    if count is not None and count.isdigit():
                        if request.user.is_authenticated:
                            cart = CartAuth(request)
                        else:
                            cart = Cart(request)
                        cart.update_count(update_pk, count)
            return JsonResponse(data)


class OrderPost(SingleObjectMixin):
    payment_type_crutch = {
        'bank' : 'Банковской картой онлайн', 
        'bill': 'Оплата по счету', 
        'receipt': 'Оплата при получении'
    }
    def post(self, request, *args, **kwargs):
        def _get_total_price(ordered_products):
            total_price = 0
            for ordered_product in ordered_products:
                total_price += ordered_product.total
            return total_price
        if request.user.is_authenticated:
            cart = CartAuth(request)
        else:
            cart = Cart(request)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            fullname = order_form.cleaned_data['fullname']
            email = order_form.cleaned_data['email']
            phone = order_form.cleaned_data['phone']
            user = None
            if request.user.is_authenticated:
                user = request.user
            elif User.objects.get(username=email).exists():
                return redirect(reverse('account:login'))
            else:
                password = User.objects.make_random_password()
                user = User.objects.create_user(email, email, password)
                profile = Profile(user=user, phone=phone)
                profile.save()
                user.last_name=fullname
            postcode = order_form.cleaned_data.get('postcode')
            region = order_form.cleaned_data.get('region')
            area = order_form.cleaned_data.get('area')
            city = order_form.cleaned_data.get('city')
            street = order_form.cleaned_data.get('street')
            house = order_form.cleaned_data.get('house')
            building = order_form.cleaned_data.get('building')
            apartment = order_form.cleaned_data.get('apartment')
            comment = order_form.cleaned_data.get('comment')
            payment_type = order_form.cleaned_data.get('payment_type')
            entity_name = order_form.cleaned_data.get('entity_name')
            entity_inn = order_form.cleaned_data.get('entity_inn')
            entity_kpp = order_form.cleaned_data.get('entity_kpp')
            delivery = None
            entity = None
            if postcode:
                delivery = Delivery(
                    postcode=postcode, region=region, area=area,
                    city=city, street=street, house=house,
                    building=building, apartment=apartment, comment=comment
                )
                delivery.save()
            if entity_name:
                entity = Entity(title=entity_name, inn=entity_inn, kpp=entity_kpp)
                entity.save()
            
            order = Order(
                delivery=delivery, user=user, entity=entity
            )
            order.save()
            products = tuple(cart.get())
            print(tuple(products), 'ORDER PRODUCTS FOR CREATE')

            ordered_products = OrderedProducts.objects.bulk_create(
                OrderedProducts(
                    order=order, product=product, count=product.count, 
                    total=product.get_discount_price()*int(product.count)) for product in products
            )
            if payment_type in ('bank', 'bill', 'receipt'):
                payment = Payment(total=_get_total_price(ordered_products), _type=self.payment_type_crutch[payment_type])
                payment.save()
            order.payment = payment
            order.save()
            return redirect(reverse('account:ProfileOrders'))
        return redirect(reverse('account:ProfileOrders'))
           