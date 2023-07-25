from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from exam_project.blog.models import Post, Category
from .forms import CommentForm


def get_categories():
    try:
        return Category.objects.all()
    except Category.DoesNotExist:
        return None


def home_page(request):

    latest_post = Post.objects.last()
    posts = Post.objects.order_by('-created_at')[1:4]
    categories = get_categories()

    context = {
        'latest_post': latest_post,
        'posts': posts,
        'categories': categories,

    }

    return render(request, 'home-page.html', context)


def all_posts(request):
    categories = get_categories()
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/all-posts.html', context)


def latest_posts(request):
    categories = get_categories()
    latest_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'latest_posts': latest_posts,
        'categories': categories,
    }
    return render(request, 'blog/latest-posts.html', context)


def page_by_category(request, category_id):
    categories = get_categories()
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)

    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
        }
    return render(request, 'blog/posts-by-category.html', context)


def about_page(request):
    categories = get_categories()

    context = {
        'categories': categories,
    }

    return render(request, 'about.html', context)


@login_required
def post_detail(request, pk):
    categories = get_categories()
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
        'categories': categories,
    }

    return render(request, 'blog/post-detail.html', context)
