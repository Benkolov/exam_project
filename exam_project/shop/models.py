from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.sku}'


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        # добавете или премахнете размери, както е необходимо
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.size}'


class Cart(models.Model):
    profile = models.OneToOneField('user.Profile', null=True, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.profile.user.username}\'s Cart'



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product_variant} x {self.quantity}'
