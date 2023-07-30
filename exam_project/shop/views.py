from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from .models import Product, ProductSize, Cart, CartItem


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'


class CartView(DetailView):
    model = Cart
    template_name = 'shop/cart.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        return self.request.user.profile.cart


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product_size = get_object_or_404(ProductSize, product=product, size=kwargs.get('size'))

        if hasattr(request.user, 'profile'):
            profile = request.user.profile
        else:
            # Ако потребителят няма профил, създайте един или върнете грешка
            # profile = Profile.objects.create(user=request.user) или
            raise Http404("Profile does not exist")

        if hasattr(profile, 'cart'):
            cart = profile.cart
        else:
            cart = Cart.objects.create(profile=profile)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_size=product_size)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product_size = get_object_or_404(ProductSize, product=product, size=kwargs.get('size'))
        cart_item = get_object_or_404(CartItem, cart=request.user.profile.cart, product_size=product_size)
        cart_item.delete()
        return redirect('cart')


