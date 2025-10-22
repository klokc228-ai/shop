from django.shortcuts import render, get_object_or_404, redirect
from .models import Rewiew, Product, CartItem
from .forms import RewiewForm, ProductForm, OrderForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


def logout_view(request):
    logout(request)
    messages.info(request, '🚪 Вы вышли из аккаунта')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, '❌ Пароли не совпадают')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Такой пользователь уже существует')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, '🎉 Вы успешно зарегистрировались!')
        return redirect('home')

    return render(request, 'main/register.html')

def home(request):
    return render(request, 'main/index.html')


def leave_review(request):
    if request.method == 'POST':
        form = RewiewForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/leave_review.html')
    else:
        form = RewiewForm()
    return render(request, 'main/leave_review.html', {'form': form})


def rewiews(request):
    reviews = Rewiew.objects.all().order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews})


def about(request):
    return render(request, 'main/about.html')


def shop(request):
    products = Product.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductForm()
    return render(request, 'main/shop.html', {'form': form, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'main/product_detail.html', {'product': product})


def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')

def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    session_key = item.session_key
    item.delete()

    total_price = sum(i.total_price() for i in CartItem.objects.filter(session_key=session_key))

    return JsonResponse({
        'success': True,
        'total': float(total_price)
    })

def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    item.save()

    session_key = request.session.session_key
    total_price = sum(i.total_price() for i in CartItem.objects.filter(session_key=session_key))

    return JsonResponse({
        'success': True,
        'quantity': item.quantity,
        'item_total': float(item.total_price()),
        'total': float(total_price)
    })

def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()


            cart_items.delete()

            return render(request, 'main/order_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'main/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })

def privacy(request):
    return render(request, 'main/privacy.html')