from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm


def home_page(request):

    latest_post = Post.objects.last()
    posts = Post.objects.order_by('-created_at')[1:4]

    context = {
        'latest_post': latest_post,
        'posts': posts,
    }

    return render(request, 'home-page.html', context)


def all_posts(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/all-posts.html', context)


def latest_posts(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/latest-posts.html', context)


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/posts-by-category.html', context)


def about_page(request):

    return render(request, 'blog/../../templates/about.html')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog/post-detail.html', context)
