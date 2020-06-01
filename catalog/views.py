from django.shortcuts import render
from django.db.models import Max, Min, Q
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, View
from .models import Category, Field, FieldType, Product, ProductBrand, ProductCountry
from django.http import JsonResponse
from .modules.args_parse import Parse
from django.template.loader import get_template
from django.core.paginator import Paginator
from .modules.post_actions import PostActions
from .compare import Compare, CompareAuth
from .favorites import Favorites, FavoritesAuth
from dto import  settings
from django.views.generic.detail import SingleObjectMixin

   
class CategoryDetailView(PostActions, ListView):
    template_name = 'category_products_list.html'
    model = Product
    paginate_by = 2

    def get_queryset(self, filter=dict(), sort=''):
        queryset = super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
        if filter:
            if filter['price_min'] and filter['price_max']:
                queryset = queryset.filter(price__gte=filter['price_min'].replace(' ', ''), price__lte=filter['price_max'].replace(' ', ''))
            if filter['brand']:
                queryset = queryset.filter(brand__title__in=filter['brand'])
            if filter['country']:
                queryset = queryset.filter(country__title__in=filter['country'])
            if filter['field_type'] and filter['field_value']:
                print(filter['field_value'])
                queryset = queryset.filter(
                    pk__in=(Field.objects.filter(
                        product__in=queryset.values_list("pk", flat=True)
                        ).filter(field_type__title__in=filter['field_type'], value__in=filter['field_value'])).values_list("product", flat=True))
            if filter['sort'] and filter['sort'] != 'default':
                if filter['sort']=='price_up':
                    queryset = queryset.order_by('price')
                elif filter['sort']=='price_down':
                    queryset = queryset.order_by('-price')
                elif filter['sort']=='title_up':
                    queryset = queryset.order_by('-title')
                elif filter['sort']=='title_down':
                    queryset = queryset.order_by('title')
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        if context['object_list'] is not None:
            filter_brands = ProductBrand.objects.filter(pk__in=context['object_list'].values_list("brand", flat=True)).only('title')
            context['filter_brands'] = filter_brands
            filter_countryes = ProductCountry.objects.filter(pk__in=context['object_list'].values_list("country", flat=True)).only('title')
            context['filter_countryes'] = filter_countryes
            filter_fields_queryset = Field.objects.filter(product__in=context['object_list'].values_list("pk", flat=True)).only('field_type', 'value')
            filter_fields = dict()
            for field in filter_fields_queryset:
                if field.field_type.title not in filter_fields:
                    filter_fields[field.field_type.title] = list()
                if field.value not in filter_fields[field.field_type.title]:
                    filter_fields[field.field_type.title].append(field.value)
            context['filter_fields'] = filter_fields
            filter_price = context['object_list'].only('price').aggregate(Min('price'), Max('price'))
            context['filter_price'] = filter_price
        if request.is_ajax():
            data_view_type = request.GET.get('data_view')
            if data_view_type is not None:
                context["view"] = data_view_type
            else:
                context["view"] = 'tile'
            filter = Parse(request.GET)
            filter.parse_args()
            context['object_list'] = self.get_queryset(filter.__dict__)
            count = len(context['object_list'])
            paginator = Paginator(context['object_list'], 2)
            page_num = request.GET.get('page')
            if page_num is not None and page_num.isdigit():
                page = paginator.page(int(page_num))
            else:
                page = paginator.page(1)
            paginator_context = dict()
            paginator_context['paginator'] = paginator
            paginator_context['page'] = page
            context['object_list'] = page.object_list
            return JsonResponse({
                'products': get_template('ajax_products.html').render(context=context, request=request), 
                'paginator': get_template('ajax_product_list_paginator.html').render(context=paginator_context, request=request),
                'count': count,
                })
        else:
            context["view"] = 'tile'
            paginator = Paginator(context['object_list'], 2)
            page = paginator.page(1)
            context['object_list'] = page.object_list
            context['page'] = page
            return render(request, self.template_name, context)

   
class CompareTemplateView(PostActions, View):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            compare = CompareAuth(request)
            # cmpr = Compare(request)
            # cmpr._clear()
            # compare._clear()
        else:
            compare = Compare(request)
            # compare._clear()
        context = dict()
        context["products"] = compare
        return render(request, self.template_name, context)
        

class FavoritesTemplateView(PostActions, View):
    template_name = 'collection.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            favorites = FavoritesAuth(self.request)
        else:
            favorites = Favorites(self.request)
        context = dict()
        context["products"] = favorites.get()
        print(context['products'])
        print(request.session[settings.FAVORITES_SESSION_ID], 'fav')
        return render(request, self.template_name, context)
    


class CategoryListTemplateView(TemplateView, SingleObjectMixin):
    template_name = 'categories.html'
    def get_context_data(self, **kwargs):
        return {}
    def post(self, request, *args, **kwargs):
        text = request.POST.get('q')
        if text is not None:
            context = {}
            products = Product.objects.filter(Q(title__icontains=text) | Q(about__icontains=text) | Q(brand__title__icontains=text))
            paginator = Paginator(products, 2)
            page = paginator.page(1)
            context['page'] = page
            context['text'] = text
            if request.is_ajax():
                page_num = request.POST.get('page')
                if page_num is not None:
                    page = paginator.page(page_num)   
                    context['page'] = page
                    return JsonResponse({
                        'products': get_template('ajax_search_products.html').render(context=context, request=request), 
                        'paginator': get_template('ajax_product_list_paginator.html').render(context=context, request=request),
                    })      

            return render(request, 'search.html', context)
        return render(request, self.template_name)

    
    
class ProductDetailView(PostActions, DetailView):
    template_name = 'product.html'
    model = Product

