from django.contrib import admin
from .models import Category, Field, FieldType, Product, ProductImage, ProductBrand, ProductCountry
from django.db import models


class FieldInline(admin.TabularInline):
    model = Field
    ordering = ('field_type', 'value', 'product')


class ImagesInline(admin.TabularInline):
    model = ProductImage


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    

def duplicate_selected(modeladmin, request, queryset):
    Product.objects.bulk_create(
        Product(
            title=product.title, category=product.category, count=product.count,
            bestseller=product.bestseller, vendor_code=product.vendor_code,
            code=product.code, price=product.price, brand=product.brand,
            country=product.country, unit=product.unit, about=product.about,
            discount_multiplier=product.discount_multiplier
        ) for product in queryset
    )
duplicate_selected.short_description = 'Дублировать выделенные товары'


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        FieldInline,
        ImagesInline,
    ]
    list_filter = ['brand', 'country']
    search_fields = ['title', 'about', 'code', 'vendor_code']
    sortable_by = ['title', 'count', 'price', 'add_date']
    list_display = [
        'title', 'price', 'count', 'bestseller', 'discount_multiplier',
        'slug', 'unit', 'add_date', 'country', 'brand',
    ]
    list_editable = [
        'price', 'discount_multiplier',
         'bestseller', 'count', 'slug',
    ]
    actions = [duplicate_selected,]





class ProductBrandAdmin(admin.ModelAdmin):
     def has_module_permission(self, request):
        return False


class ProductCountryAdmin(admin.ModelAdmin):
     def has_module_permission(self, request):
        return False

class FieldTypeAdmin(admin.ModelAdmin):
     def has_module_permission(self, request):
        return False


admin.site.register(FieldType, FieldTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductCountry, ProductCountryAdmin)