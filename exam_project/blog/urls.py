from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('about/', about_page, name='about'),
    path('all/', all_posts, name='all'),
    path('latest-posts/', latest_posts, name='latest_posts'),
    path('category/<int:category_id>/', posts_by_category, name='posts_by_category'),

]
