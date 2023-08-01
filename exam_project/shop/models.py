from django.db import models
from slugify import slugify


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.sku}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.sku}'


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
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

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.cart.profile.user.username}\'s Cart Item'

    def total_price(self):
        return self.product_size.product.price * self.quantity

