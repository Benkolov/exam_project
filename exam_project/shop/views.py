from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UpdateCartForm
from .models import Product, ProductSize, Cart, CartItem

from django.core.mail import send_mail
from django.template.loader import render_to_string

from ..blog.views import get_categories


def product_list_view(request):
    categories = get_categories()
    products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'shop/product_list.html', context)


def product_detail_view(request, slug):
    categories = get_categories()
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,
        'categories': categories,
    }

    return render(request, 'shop/product_detail.html', context)


@login_required
def cart_view(request):
    categories = get_categories()

    if not hasattr(request.user, 'profile'):
        raise Http404("Profile does not exist")
    cart = request.user.profile.cart
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.quantity * item.product_size.product.price
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': categories,
    }
    return render(request, 'shop/cart.html', context)


@login_required
def add_to_cart_view(request, slug, size):
    product = get_object_or_404(Product, slug=slug)
    product_size = get_object_or_404(ProductSize, product=product, size=size)

    if not hasattr(request.user, 'profile'):
        raise Http404("Profile does not exist")

    profile = request.user.profile

    if not hasattr(profile, 'cart'):
        cart = Cart.objects.create(profile=profile)
    else:
        cart = profile.cart

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_size=product_size)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart_view(request, slug, size):
    product = get_object_or_404(Product, slug=slug)
    product_size = get_object_or_404(ProductSize, product=product, size=size)
    cart_item = get_object_or_404(CartItem, cart=request.user.profile.cart, product_size=product_size)
    cart_item.delete()
    return redirect('cart')


@login_required
def update_cart_view(request, slug, size):
    if request.method != 'POST':
        raise Http404

    product = get_object_or_404(Product, slug=slug)
    product_size = get_object_or_404(ProductSize, product=product, size=size)
    cart_item = get_object_or_404(CartItem, cart=request.user.profile.cart, product_size=product_size)

    form = UpdateCartForm(request.POST)
    if form.is_valid():
        new_quantity = form.cleaned_data['quantity']
        if new_quantity > product_size.stock:
            messages.error(request, 'You cannot add more items than available in stock.')
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

    return redirect('cart')


@login_required
def complete_order_view(request):
    user = request.user
    if not user.profile.address or not user.profile.phone:
        messages.error(request, "Please complete your address and phone number before completing the order.")
        return redirect('profile')

    cart = request.user.profile.cart
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.quantity * item.product_size.product.price

    context = {
        'user': user,
        'items': cart_items,
        'total_price': sum(item.total_price for item in cart_items),
    }
    message = render_to_string('email/order_confirmation.txt', context)
    send_mail(
        'Order Confirmation',
        message,
        'from@example.com',
        ['to@example.com']
    )

    messages.success(request, "Your order has been completed successfully.")
    return redirect('home')




