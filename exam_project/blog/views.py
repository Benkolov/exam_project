from django.shortcuts import render
from .models import Post


def home_page(request):

    return render(request, 'home-page.html')


def post_detail(request, pk):

    post = Post.objects.get(pk=pk)

    return render(request, 'blog/post-detail.html', {'post': post})
