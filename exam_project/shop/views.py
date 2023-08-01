from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, ProductSize, Cart, CartItem


# class ProductListView(ListView):
#     model = Product
#     template_name = 'shop/product_list.html'
#     context_object_name = 'products'
#
#
# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'shop/product_detail.html'
#     context_object_name = 'product'
#
#
# class CartView(DetailView):
#     model = Cart
#     template_name = 'shop/cart.html'
#     context_object_name = 'cart'
#
#     def get_object(self, queryset=None):
#         return self.request.user.profile.cart
#
#
# class AddToCartView(View):
#     def get(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, pk=kwargs.get('pk'))
#         product_size = get_object_or_404(ProductSize, product=product, size=kwargs.get('size'))
#
#         if hasattr(request.user, 'profile'):
#             profile = request.user.profile
#         else:
#             raise Http404("Profile does not exist")
#
#         if hasattr(profile, 'cart'):
#             cart = profile.cart
#         else:
#             cart = Cart.objects.create(profile=profile)
#
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product_size=product_size)
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()
#         return redirect('shop:cart')
#
#
# class RemoveFromCartView(View):
#     def get(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, pk=kwargs.get('pk'))
#         product_size = get_object_or_404(ProductSize, product=product, size=kwargs.get('size'))
#         cart_item = get_object_or_404(CartItem, cart=request.user.profile.cart, product_size=product_size)
#         cart_item.delete()
#         return redirect('shop:cart')


def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def cart_view(request):
    if not hasattr(request.user, 'profile'):
        raise Http404("Profile does not exist")
    cart = request.user.profile.cart
    return render(request, 'shop/cart.html', {'cart': cart})


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
def remove_from_cart_view(request, pk, size):
    product = get_object_or_404(Product, pk=pk)
    product_size = get_object_or_404(ProductSize, product=product, size=size)
    cart_item = get_object_or_404(CartItem, cart=request.user.profile.cart, product_size=product_size)
    cart_item.delete()
    return redirect('cart')
