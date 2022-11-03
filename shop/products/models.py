from django.db import models
from users.models import User
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Категория устройства")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание категории устройста")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания категории")

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('product_list_by_category',
                       args=[self.slug])

    class Meta:
        verbose_name = "Категория устройства"
        verbose_name_plural = "Категории устройств"
        ordering = ['-time']


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField(upload_to='device_image/%Y', blank=True, verbose_name='Фото')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Краткое описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    quantity = models.IntegerField(default=0, verbose_name="Количество")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time']


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_database = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} |\
    Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'Товар в корзину'
        verbose_name_plural = 'Корзина'
