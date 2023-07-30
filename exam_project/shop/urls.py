from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, AddToCartView, RemoveFromCartView

app_name = 'shop'

urlpatterns = [
    path('all_product', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<int:pk>/<str:size>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:pk>/<str:size>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]



