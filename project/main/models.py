from django.db import models
from PIL import Image
from rembg import remove
import io

class Rewiew(models.Model):
    name = models.CharField(max_length=50, default='Anonymous')
    title = models.CharField(max_length=50)
    about = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(default=5) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.title}"
    
    class Meta:
        verbose_name = 'Rewiew'
        verbose_name_plural = 'Rewiews'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

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
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} — {self.name}"


    