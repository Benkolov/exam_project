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
        try:
            product = Product.objects.get(pk=kwargs.get('pk'))
        except Product.DoesNotExist:
            raise Http404(f"No Product found with pk {kwargs.get('pk')}")

        try:
            product_variant = ProductSize.objects.get(product=product, size=kwargs.get('size'), color=kwargs.get('color'))
        except ProductSize.DoesNotExist:
            raise Http404(f"No ProductVariant found for Product {product.id} with size {kwargs.get('size')} and color {kwargs.get('color')}")

        cart_item, created = CartItem.objects.get_or_create(cart=request.user.profile.cart, product_variant=product_variant)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')



class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product_variant = get_object_or_404(ProductSize, product=product, size=kwargs.get('size'), color=kwargs.get('color'))
        cart_item = get_object_or_404(CartItem, cart=request.user.cart, product_variant=product_variant)
        cart_item.delete()
        return redirect('cart')

