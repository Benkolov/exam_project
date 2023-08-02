from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('about/', about_page, name='about'),
    path('all/', all_posts, name='all'),
    path('latest-posts/', latest_posts, name='latest_posts'),
    path('category/<int:category_id>/', page_by_category, name='posts_by_category'),
    path('posts_by_tag/<str:tag_slug>/', posts_by_tag, name='posts_by_tag'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', delete_comment, name='delete_comment'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/edit/', edit_comment, name='edit_comment'),
    path('search/', search_results, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
