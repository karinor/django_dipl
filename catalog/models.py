from dto.settings import STATIC_ROOT
from django.db import models
from django.utils import timezone
import os



# Create your models here.
class Category(models.Model):
    SPRITE_CHOICES = [
        ('category-icon-1', 'category-icon-1'),
        ('category-icon-2', 'category-icon-2'),
        ('category-icon-3', 'category-icon-3'),
        ('category-icon-4', 'category-icon-4'),
        ('category-icon-5', 'category-icon-5'),
        ('category-icon-6', 'category-icon-6'),
        ('category-icon-7', 'category-icon-7'),
        ('category-icon-8', 'category-icon-8'),
        ('category-icon-9', 'category-icon-9'),
        ('category-icon-10', 'category-icon-10'),
        ('category-icon-11', 'category-icon-11'),
        ('done_icon', 'done_icon'),
        ('exit-icon', 'exit-icon'),
        ('file-icon', 'file-icon'),
        ('heart-icon', 'heart-icon'),
        ('mail', 'mail'),
        ('no_photo', 'no_photo'),
        ('phone', 'phone'),
        ('wallet', 'wallet')
    ]

    title = models.CharField(max_length=60,  verbose_name='Название категории')
    about = models.TextField(verbose_name='Описание категории', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name='Родитель', null=True, blank=True)
    svg = models.CharField(max_length=16, choices=SPRITE_CHOICES, default = 'no_photo')
    image = models.ImageField(upload_to='images/categories', default='catalog-block-img1.jpg')
    slug = models.SlugField(allow_unicode=False, unique=True, max_length=150)

    class Meta:
        ordering = ["title"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории товаров"

    def get_childs(self):
        return Category.objects.filter(parent=self.pk)

    def get_absolute_url(self):
        return "/catalog/%s" % self.slug

    def childs_exists(self):
        # self == Category
        return Category.objects.filter(parent=self.pk).exists()

    def __str__(self):
        return self.title


class ProductCountry(models.Model):
    svg_flag = models.FileField(upload_to='images/countries', max_length=100, verbose_name='Флаг в формате .svg')
    title = models.CharField(max_length=50, verbose_name='Название страны')


    class Meta:
        verbose_name = "Страна продукта"
        verbose_name_plural = "Страны продуктов"

    def __str__(self):
        return self.title


class ProductBrand(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название брэнда')


    class Meta:
        verbose_name = "Бренд продукта"
        verbose_name_plural = "Бренды продуктов"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=80, verbose_name='Название товара')
    vendor_code = models.CharField(max_length=60, verbose_name='Артикул', null=True)
    code = models.CharField(max_length=8, verbose_name='Код', null=True)
    price = models.PositiveIntegerField(verbose_name='Цена', null=True)
    count = models.PositiveIntegerField(verbose_name='Кол-во на складе', null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    bestseller = models.BooleanField(verbose_name='Лидер продаж', blank=True, default=False)
    discount_multiplier = models.FloatField(default=1.0, blank=True, verbose_name='Множитель скидки (1.0=нет скидки)')
    add_date = models.DateField(auto_now_add=True, editable=False, verbose_name='Дата добавления на сайт')
    image = models.ImageField(default=os.path.join(STATIC_ROOT,'images','default-image.jpg'), upload_to='images/products', verbose_name='Изображение товара', null=True)
    slug = models.SlugField(allow_unicode=False, unique=True, max_length=150, blank=True, null=True, verbose_name='Ссылка (Латиница)')
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, null=True, verbose_name='Брэнд')
    country = models.ForeignKey(ProductCountry, on_delete=models.SET_NULL, null=True, verbose_name='Страна')
    about = models.TextField(verbose_name='Описание товара', null=True, blank=True)
    unit = models.CharField(verbose_name='Единица измерения', max_length=10)

    class Meta:
        ordering = ["title"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def is_new(self):
        return (timezone.now().date() - self.add_date).days < 3

    def get_discount_price(self):
        return int(self.price*self.discount_multiplier)

    def get_wholesale_price(self):
        return int(self.get_discount_price()*0.95)

    def get_wholesale_price_default(self):
        return int(self.price*0.95)

    def get_vip_price(self):
        return int(self.get_discount_price()*0.9)

    def get_vip_price_default(self):
        return int(self.price*0.9)

    def get_images(self):
        return ProductImage.objects.filter(product=self.pk)

    def get_fields(self):
        return Field.objects.filter(product=self.pk)

    #Ограничить поля только для превью
    def get_best_offers(self):
        return Product.objects.filter(category=self.category, bestseller=True).exclude(pk=self.pk).only(
            'title', 'price', 'bestseller', 'add_date', 
            'image', 'discount_multiplier', 'count', 
            'country', 'brand')
    
    def __str__(self):
        return self.title


class FieldType(models.Model):
    title = models.CharField(max_length=20,  verbose_name='Название свойства товара')


    class Meta:
        ordering = ["title"]
        verbose_name = "Названия свойств товаров"
        verbose_name_plural = "Название свойства товара"

    def __str__(self):
        return self.title


class Field(models.Model):
    field_type = models.ForeignKey(FieldType, on_delete=models.PROTECT, verbose_name='Название поля')
    value = models.CharField(max_length=50, verbose_name='Значение поля')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт') 


    class Meta:
        verbose_name = "Свойства товара"
        verbose_name_plural = "Свойство товара"

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/product_images/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')


    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    def __str__(self):
        return str(self.image)
    



