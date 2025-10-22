from django.contrib import admin
from .models import Rewiew, Product, CartItem, Order

@admin.register(Rewiew)
class RewiewAdmin(admin.ModelAdmin):
    list_display = ('title', 'about')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'session_key')
    search_fields = ('product__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'total_price', 'created_at')
    search_fields = ('name', 'phone', 'address')