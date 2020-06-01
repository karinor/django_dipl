from django.shortcuts import render
from django.views.generic import TemplateView
from catalog.models import Product
from catalog.modules.post_actions import PostActions
from .models import Brands, IndexPageSlider

# Create your views here.

class IndexView(PostActions, TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['best_offers'] = {
            'bestseller': Product.objects.filter(bestseller=True)[:9], 
            'discount': Product.objects.exclude(discount_multiplier=1.0).order_by('-discount_multiplier')[:9],
            'new': Product.objects.order_by('-add_date')[:9],
        }
        context['slides'] = IndexPageSlider.objects.all()
        return context


class ClientamView(TemplateView):
    template_name = 'clientam.html'


class ContactsView(TemplateView):
    template_name = 'contacts.html'


class BrandsView(TemplateView):
    template_name = 'brands.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['brands'] = Brands.objects.all()
        return context