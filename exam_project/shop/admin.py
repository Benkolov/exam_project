from django.contrib import admin
from .models import Product, ProductSize, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'color')
    list_filter = ('name', 'sku', 'color')
    ordering = ('name',)


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'stock')
    list_filter = ('product', 'size',)
    ordering = ('product',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('get_username',)

    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'  # Sets the column header in the admin interface



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity')
    list_filter = ('cart', 'product_variant')
