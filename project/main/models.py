from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from rembg import remove
import io


class Rewiew(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )  
    name = models.CharField(max_length=50, default='Anonymous', verbose_name='Имя пользователя')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    about = models.TextField(max_length=500, verbose_name='Отзыв')
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_site_review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.title}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='products/', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            try:
                image_path = self.photo.path
                with open(image_path, "rb") as inp:
                    output = remove(inp.read())
                    img = Image.open(io.BytesIO(output)).convert("RGBA")
                img.save(image_path, format="PNG")
                print(f"✅ Фон успешно удалён для {self.name}")
            except Exception as e:
                print(f"⚠️ Ошибка при удалении фона у {self.name}: {e}")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    session_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} — {self.quantity} шт.'

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Корзина'



class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return f"Заказ №{self.id} — {self.name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
