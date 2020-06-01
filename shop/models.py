from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Delivery(models.Model):
    postcode = models.CharField(verbose_name='Почтовый индекс', max_length=10)
    region = models.CharField(verbose_name='Область', max_length=50)
    area = models.CharField(verbose_name='Район', max_length=50, blank=True, null=True)
    city = models.CharField(verbose_name='Город/Населенный пункт', max_length=50)
    street = models.CharField(verbose_name='Улица', max_length=50)
    house = models.CharField(verbose_name='Дом', max_length=10)
    building = models.CharField(verbose_name='Корпус', max_length=20)
    apartment = models.CharField(verbose_name='Квартира', max_length=10)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)


    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"
    
    def __str__(self):
        return f'{self.postcode} {self.region} г. {self.city}, д. {self.house}/{self.building}, кв. {self.apartment}'


class Payment(models.Model):
    PAYMENT_TYPE = [
        ('Банковской картой онлайн', 1),
        ('Оплата по счету', 2),
        ('Оплата при получении', 3),
    ]
    _type = models.CharField(choices=PAYMENT_TYPE, verbose_name='Тип оплаты', max_length=30, default='Оплата при получении')
    total = models.PositiveIntegerField(verbose_name='Сумма')
    paid = models.BooleanField(verbose_name='Оплачено', default=False, blank=True)


    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"
    
    def __str__(self):
        if self.paid:
            paid = 'Да'
        else:
            paid = 'Нет'
        return f'{self._type} Сумма: {self.total} Оплачено: {paid}'


class Entity(models.Model):
    title = models.CharField(verbose_name='Название органищации', max_length=60)
    inn = models.CharField(verbose_name='ИНН', max_length=13)
    kpp = models.CharField(verbose_name='КПП', max_length=20)


    class Meta:
        verbose_name = "Юр. лицо"
        verbose_name_plural = "Юр. лица"

    def __str__(self):
        return self.title

class Order(models.Model):
    ORDER_STATUS = [
        (1, 'В обработке'),
        (2, 'Выполнен'),
        (3, 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, verbose_name='Доставка', blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='Оплата', blank=True, null=True)
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, verbose_name='Юридическое лицо', blank=True, null=True)
    date = models.DateField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.PositiveSmallIntegerField(verbose_name='Статус заказа', choices=ORDER_STATUS, default=1, blank=True)


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return f'Заказ №{self.id} от {self.date}'


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.PositiveIntegerField(verbose_name='Количество')
    total = models.PositiveIntegerField(verbose_name='Цена позиции')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')


    class Meta:
        verbose_name = "Заказанный продукт"
        verbose_name_plural = "Заказанные продукты"

    def __str__(self):
        return f'Заказ №{self.order.id}; Продукт: {self.product} x{self.count}'
