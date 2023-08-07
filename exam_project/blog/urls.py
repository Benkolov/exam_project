from django.urls import path

from .views import home_page, post_detail, about_page, all_posts, latest_posts, page_by_category, posts_by_tag, \
    delete_comment, edit_comment, search_results, news_list, news_detail, gallery, news_by_tag

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name='home'),
    path('post/<str:slug>/', post_detail, name='post_detail'),
    path('about/', about_page, name='about'),
    path('all/', all_posts, name='all'),
    path('latest-posts/', latest_posts, name='latest_posts'),
    path('category/<int:category_id>/', page_by_category, name='posts_by_category'),
    path('posts_by_tag/<str:tag_slug>/', posts_by_tag, name='posts_by_tag'),
    path('<str:content_type>/<int:content_pk>/comment/<int:comment_pk>/delete/', delete_comment, name='delete_comment'),
    path('<str:content_type>/<int:content_pk>/comment/<int:comment_pk>/edit/', edit_comment, name='edit_comment'),
    path('search/', search_results, name='search'),
    path('news/', news_list, name='news_list'),
    path('news/<str:slug>/', news_detail, name='news_detail'),
    path('news_by_tag/<str:tag_slug>/', news_by_tag, name='news_by_tag'),
    path('gallery/', gallery, name='gallery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
