from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Производитель")
    country = models.CharField(max_length=100, verbose_name="Страна")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.country})"


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название игры")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    min_players = models.PositiveIntegerField(default=1, verbose_name="Мин. игроков")
    max_players = models.PositiveIntegerField(default=4, verbose_name="Макс. игроков")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='products', verbose_name="Производитель")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['id']

    def __str__(self):
        return self.name


class WarehouseStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='warehouse', verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")

    class Meta:
        verbose_name = "Складской остаток"
        verbose_name_plural = "Складские остатки"

    def __str__(self):
        return f"Склад: {self.product.name} — {self.quantity} шт."


class Promocode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка (%)")
    expires_at = models.DateField(verbose_name="Действителен до")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"


class OrderStatus(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Покупатель")
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, related_name='orders', verbose_name="Статус")
    promocode = models.ForeignKey(Promocode, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders', verbose_name="Промокод")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    delivery_address = models.CharField(max_length=300, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders', verbose_name="Товары в заказе")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"

    def __str__(self):
        return f"Корзина {self.user.username}: {self.product.name} ({self.quantity})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    rating = models.PositiveIntegerField(verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name} ({self.rating}/5)"