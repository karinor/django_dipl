from django.conf import settings
from django.db.models.signals import pre_init

from catalog.models import Product
from pprint import pprint
from math import trunc
from account.models import Cart as CartModel

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cashe_products = None
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def get(self):
        return self._get_products_with_count(self.cart, Product.objects.filter(id__in=map(self._get_ids_from_session, self.cart)))

    def add(self, product_id, count=None):
        product_index = self._get_index_from_session(product_id, self.cart)
        if product_index == -1:
            self.cart.append([product_id, 1 if count is None else count if count.isdigit() else 1])
            self._save()
        elif count is not None:
            self.cart[product_index][1] = count
            self._save()
    
    def remove(self, product_id):
        product_index = self._get_index_from_session(product_id, self.cart)
        if product_index != -1:
            del self.cart[product_index]
            self._save()
    
    def update_count(self, product_id, count):
        product_index = self._get_index_from_session(product_id, self.cart)
        if product_index != -1 and count.isdigit():
            self.cart[product_index][1] = count
            self._save()

    def _get_products_with_count(self, cart, product_objects):
        for product in product_objects:
            product_id = product.id
            for item in cart:
                result = self._srch_id_in_cart(product_id, item)
                if result is not None:
                    break
            if result is not None:
                product.count = result[1]
                yield product
    
    def _get_ids_from_session(self, session_cart_obj):
        return session_cart_obj[0]

    def index_of(self, obj):
        try:
            return self.cart.index(obj)
        except ValueError:
            return -1

    def _srch_id_in_cart(self, obj_id, obj):
        if int(obj_id) == int(obj[0]):
            return obj

    def _cashe(self):
            if self.cashe_products is None:
                product_model_objects = Product.objects.filter(id__in=map(self._get_ids_from_session, self.cart))
                self.cashe_products = product_model_objects
                return self.cashe_products
            else:
                return self.cashe_products

    def _get_index_from_session(self, product_id, session):
        try:
            res_list = list(map(self._srch_id_in_cart, [product_id] * len(session), session))
            while None in res_list:
                res_list.remove(None)
            results = next(iter(res_list))
        except (ValueError, StopIteration):
            try:
                results = next(iter(map(self._srch_id_in_cart, [product_id] * len(session), session)))
            except StopIteration:
                results = None
        return self.index_of(results)

    def _save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def _discount_check(self, price):
        price_with_discount = 0
        if price > 12000:
            price_with_discount = int(price * 0.9)
        elif price > 1999:
            price_with_discount = int(price * 0.95)
        else:
            price_with_discount = int(price)

        return price_with_discount

    def get_total_price(self):
        product_model_objects = self._cashe()
        products = self._get_products_with_count(self.cart, product_model_objects)
        total_price = sum(
            float(product.price) * float(product.discount_multiplier) * float(product.count) for product in products
        )
        return self._discount_check(total_price)
        
    def get_total_discount(self):
        product_model_objects = self._cashe()
        total_discount = sum(
            product.price for product in product_model_objects
        ) - self.get_total_price()
        return total_discount
 
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        for item in self.cart:
            yield item
    
    def __len__(self):
        return len(self.cart)


class CartAuth:
    def __init__(self, request):
        self.request = request
        self.cashe_products = None
        self.session = request.session
        session_cart = list(Cart(request))
        self.cart = session_cart
        create_items = None
        if len(session_cart) > 0:
            model_objects = CartModel.objects.filter(user=request.user)
            model_ids = [
                item.product.pk for item in model_objects
            ]
            session_products = map(self._get_ids_from_session, session_cart)
            session_products_set = set(session_products)
            model_ids_set = set(model_ids)
            items_intersection = model_ids_set | session_products_set
            ids_for_add = list(items_intersection - model_ids_set)
            products_objects = Product.objects.filter(id__in=ids_for_add)
          
            products_for_add = self._get_products_with_count(session_cart, products_objects)
            while None in products_for_add:
                products_for_add.remove(None)
            create_items = CartModel.objects.bulk_create(
                CartModel(user=request.user, product=product, count=product.count) for product in products_for_add
            )

            #брать из базы
        self.cart = [
            [item.product.id, item.count] for item in CartModel.objects.filter(user=request.user)
        ]
        self._save()
    
    def get(self):
        return self._get_products_with_count(self.cart, (item.product for item in CartModel.objects.filter(user=self.request.user)))

    def _get_products_with_count(self, cart, product_objects):
        for product in product_objects:
            product_id = product.id
            res_list = []
            for item in self.cart:
                result = self._srch_id_in_cart(product_id, item)
                if result is not None:
                    break
            else:
                result = None
            if result is not None:
                product.count = result[1]
                yield product
    
    def _get_ids_from_session(self, session_cart_obj):
        return session_cart_obj[0]

    def index_of(self, obj):
        try:
            return self.cart.index(obj)
        except ValueError:
            return -1

    def _srch_id_in_cart(self, obj_id, obj):
        if obj_id == obj[0]:
            return obj

    def _get_index_from_session(self, product_id, session):
        try:
            res_list = list(map(self._srch_id_in_cart, [product_id] * len(session), session))
            res_list.remove(None)
            results = next(iter(res_list))
        except ValueError:
            results = next(iter(map(self._srch_id_in_cart, [product_id] * len(session), session)))
        return self.index_of(results)

    def add(self, product_id, count=None):
        if not CartModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            added = CartModel.objects.create(user=self.request.user, product_id=product_id, count=1 if count is None else count if count.isdigit() else 1)
            added.save()
            if product_id not in tuple(self._get_ids_from_session(self.cart)):
                self.cart.append((product_id, 1 if count is None else count))
                self._save()
    
    def remove(self, product_id):
        if CartModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            CartModel.objects.filter(user=self.request.user, product_id=product_id).delete()
            product_index = self._get_index_from_session(product_id, self.cart)
            if product_index != -1:
                del self.cart[product_index]
                self._save()
    
    def update_count(self, product_id, count):
        if CartModel.objects.filter(user=self.request.user, product_id=product_id).exists() and count.isdigit():
            updated = CartModel.objects.get(product_id=product_id, user=self.request.user)
            updated.count = count
            updated.save()
            product_index = self._get_index_from_session(product_id, self.cart)
            if product_index != -1:
                self.cart[product_index][1] = count
                self._save()

    def _save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def _cashe(self):
        if self.cashe_products is None:
            product_model_objects = Product.objects.filter(id__in=map(self._get_ids_from_session, self.cart))
            self.cashe_products = product_model_objects
            return self.cashe_products
        else:
            return self.cashe_products

    def _discount_check(self, price):
        price_with_discount = 0
        if price > 12000:
            price_with_discount = int(price * 0.9)
        elif price > 1999:
            price_with_discount = int(price * 0.95)
        else:
            price_with_discount = int(price)

        return price_with_discount

    def get_total_price(self):
        product_model_objects = self._cashe()
        products = self._get_products_with_count(self.cart, product_model_objects)
        total_price = sum(
            float(product.price) * float(product.discount_multiplier) * float(product.count) for product in products
        )
        return self._discount_check(total_price)
        
    def get_total_discount(self):
        product_model_objects = self._cashe()
        total_discount = sum(
            product.price for product in product_model_objects
        ) - self.get_total_price()
        return total_discount
 
    def clear(self):
        self.cart = {}
        CartModel.objects.filter(user=self.request.user).delete()

    def __iter__(self):
        for item in self.cart:
            yield (item)
    
    def __len__(self):
        return len(self.cart)