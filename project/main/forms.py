from .models import Rewiew, Product, Order
from django import forms

class RewiewForm(forms.ModelForm):
    class Meta:
        model = Rewiew
        fields = ['title', 'about', 'name', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему отзыва'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишите ваш отзыв здесь'}),
            'rating': forms.HiddenInput(),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название продукта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание продукта'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена продукта'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }   

class OrderForm(forms.ModelForm): 
    class Meta:
        model = Order
        fields = ['name', 'phone', 'city' ,'address', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш телефон'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес доставки'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий к заказу (необязательно)',
                'rows': 3
            }),
        }