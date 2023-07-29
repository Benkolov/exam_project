from django.contrib import admin
from .models import Product, ProductVariant, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'stock')
    list_filter = ('product', 'size', 'color')
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
