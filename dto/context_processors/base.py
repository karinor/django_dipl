from django.conf import settings
from django.template.context_processors import request
from catalog.models import Category, Field, FieldType, Product
from catalog.favorites import FavoritesAuth
from catalog.compare import CompareAuth


def catalog(request):
    if request.user.is_authenticated:
        compare_count = CompareAuth(request)
    else:
        compare_count = request.session.get(settings.COMPARE_SESSION_ID)
    if request.user.is_authenticated:
        favorites_count = FavoritesAuth(request)
    else:
        favorites_count = request.session.get(settings.FAVORITES_SESSION_ID)
    cart_count = request.session.get(settings.CART_SESSION_ID)
    if compare_count is not None:
        compare_count = len(compare_count)
    else:
        compare_count = 0
    if favorites_count is not None:
        favorites_count = len(favorites_count)
    else:
        favorites_count = 0
    if cart_count is not None:
        cart_count = len(cart_count)
    else:
        cart_count = 0
        
    return {
        "catalog": Category.objects.filter(parent=None).only('title', 'image', 'svg'),
        'compare_count': compare_count,
        'favorites_count': favorites_count,
        'cart_count': cart_count
    }