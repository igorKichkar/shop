from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True)

    def __str__(self):
        return 'Покупатель: {}'.format(self.username)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Subсategory(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя подкатегории')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, verbose_name='Категория')

    def __str__(self):
        return self.slug


class Product_name(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя подкатегории')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Subсategory, on_delete=models.CASCADE, verbose_name='Название товара')

    def __str__(self):
        return self.slug


class Product(models.Model):
    class Meta:
        abstract = True

    product_name = models.ForeignKey(Product_name, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, )
    description = models.TextField(null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('detail_product',
                       kwargs={'product_name_category': self.product_name.slug, 'product_id': self.id})

    def __str__(self):
        return '{} : {}'.format(self.product_name.name, self.title)


class Notebook(Product):
    display = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')


class Smartphone(Product):
    display = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный объем встраиваемой памяти')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')


class Headphones(Product):
    interface = models.CharField(max_length=255, verbose_name='Интерфейс')


class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    total_products = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.content_object.title


class OrderProduct(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена на момент заказа')

    def __str__(self):
        return self.content_object.title


class TotalOrderForUser(models.Model):
    order = models.ManyToManyField(OrderProduct)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    time_create = models.DateTimeField(null=True, auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('detail_order', kwargs={'order_id': self.id})
