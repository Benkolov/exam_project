from django.urls import path
from .views import product_list_view, product_detail_view, cart_view, add_to_cart_view, remove_from_cart_view, \
    update_cart_view, complete_order_view

urlpatterns = [
    path('all_product', product_list_view, name='product_list'),
    path('product/<str:slug>/', product_detail_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<str:slug>/<str:size>/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/<str:slug>/<str:size>/', remove_from_cart_view, name='remove_from_cart'),
    path('update_cart/<str:slug>/<str:size>/', update_cart_view, name='update_cart'),
    path('complete_order/', complete_order_view, name='complete_order'),
]
