from django.conf import settings
from .models import Product, Field, FieldType
from pprint import pprint
from account.models import Favorites as FavModel
from django.core import serializers


class Favorites:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = []
        self.favorites = favorites
    
    def get(self):
        return Product.objects.filter(id__in=self.favorites)

    def add(self, product_id):
        if not product_id in self.favorites:
            self.favorites.append(product_id)
            self._save()
    
    def remove(self, product_id):
        if product_id in self.favorites:
            self.favorites.remove(product_id) 
            self._save()
    
    def _save(self):
        self.session[settings.FAVORITES_SESSION_ID] = self.favorites
        self.session.modified = True

    def __iter__(self):
        for item in self.favorites:
            yield int(item)
    
    def __len__(self):
        return len(self.favorites)


class FavoritesAuth:
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        session_fav = Favorites(request)
        if len(session_fav) > 0:
            model_objects = FavModel.objects.filter(user=request.user)
            model_ids = [
                favorite.product.pk for favorite in model_objects
            ]
            session_ids = tuple(iter(session_fav))
            session_ids_set = set(session_ids)
            model_ids_set = set(model_ids)
            favorites_intersection = model_ids_set | session_ids_set
            ids_for_add = list(favorites_intersection - model_ids_set)
            products_for_add = Product.objects.filter(id__in=ids_for_add)
            create_favorites = FavModel.objects.bulk_create(
                FavModel(user=request.user, product=product) for product in products_for_add
            )
        self.favorites = [
            favorite.product.pk for favorite in FavModel.objects.filter(user=request.user)
        ]
        self._save()
    
    def get(self):
        return Product.objects.filter(id__in=self.favorites)

    def add(self, product_id):
        if not FavModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            added = FavModel.objects.create(user=self.request.user, product_id=product_id)
            added.save()
            if product_id not in self.favorites:
                self.favorites.append(added.id)
                self._save()
            
    
    def remove(self, product_id):
        if FavModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            removed = FavModel.objects.filter(user=self.request.user, product_id=product_id)
            self.favorites.remove(removed[0].product.id)
            removed.delete()
            self._save()
    
    def _save(self):
        self.session[settings.FAVORITES_SESSION_ID] = self.favorites
        self.session.modified = True

    def __iter__(self):
        for item in self.favorites:
            yield item
    
    def __len__(self):
        return len(self.favorites)

            


    