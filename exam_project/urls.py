from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exam_project.shop.urls')),
    path('', include('exam_project.user.urls')),
    path('', include('exam_project.blog.urls')),

]
