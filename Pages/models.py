from django.db import models


class Brands(models.Model):
    title = models.CharField(verbose_name='Название бренда', max_length=50)
    image = models.ImageField(verbose_name='Изображение бренда', upload_to='images/products')


class IndexPageSlider(models.Model):
    models.ImageField(verbose_name='Изображение', upload_to='images/products')
    models.CharField(verbose_name='Ссылка', max_length=90)