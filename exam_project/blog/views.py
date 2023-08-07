from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from exam_project.blog.models import Post, Category, Tag, Comment, News, Gallery

from .forms import CommentForm
from ..shop.models import Product


from django.db.models import Q


def search_results(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(Q(name__icontains=query))
        posts = Post.objects.filter(Q(title__icontains=query))
        print(f'Search results for products: {products}')  # Add this line
        print(f'Search results for posts: {posts}')  # Add this line
    else:
        products = Product.objects.none()
        posts = Post.objects.none()

    context = {
        'query': query,
        'search_products': products,
        'search_posts': posts,
    }

    return render(request, 'search_results.html', context)


def get_categories():
    try:
        return Category.objects.all()
    except Category.DoesNotExist:
        return None


def home_page(request):

    latest_post = Post.objects.last()
    posts = Post.objects.order_by('-created_at')[:4]
    categories = get_categories()

    latest_products = Product.objects.order_by('-id')[:4]
    latest_news = News.objects.order_by('-id')[:4]

    context = {
        'latest_post': latest_post,
        'posts': posts,
        'categories': categories,
        'latest_products': latest_products,
        'latest_news': latest_news,

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


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'posts': posts,
    }

    return render(request, 'blog/posts_by_tag.html', context)


def about_page(request):
    categories = get_categories()

    context = {
        'categories': categories,
    }

    return render(request, 'about.html', context)


@login_required
def post_detail(request, slug):
    categories = get_categories()
    post = get_object_or_404(Post, slug=slug)
    comments = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'categories': categories,
    }

    return render(request, 'blog/post-detail.html', context)


@login_required
def delete_comment(request, content_type, content_pk, comment_pk):
    if content_type == 'news':
        content_object = get_object_or_404(News, pk=content_pk)
    elif content_type == 'post':
        content_object = get_object_or_404(Post, pk=content_pk)
    else:
        raise ObjectDoesNotExist

    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
        return redirect(f'{content_type}_detail', slug=content_object.slug)
    else:
        return HttpResponse("You don't have permission to delete this comment.")


@login_required
def edit_comment(request, content_type, content_pk, comment_pk):
    if content_type == 'news':
        content_object = get_object_or_404(News, pk=content_pk)
    elif content_type == 'post':
        content_object = get_object_or_404(Post, pk=content_pk)
    else:
        raise ObjectDoesNotExist

    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.author:
        return HttpResponseForbidden("You don't have permission to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(f'{content_type}_detail', slug=content_object.slug)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
    }

    return render(request, 'blog/edit-comment.html', context)


def news_list(request):
    news = News.objects.all().order_by('-created_at')

    context = {
        'news': news
    }

    return render(request, 'blog/news_list.html', context)


def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    comments = news_item.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user
            comment.save()
            return redirect('news_detail', slug=slug)
    else:
        form = CommentForm()

    context = {
        'news_item': news_item,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog/news_detail.html', context)


def gallery(request):
    images = Gallery.objects.all().order_by('-created_at')

    context = {
        'images': images,
    }

    return render(request, 'blog/gallery.html', context)


def news_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    news = News.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'news': news,
    }

    return render(request, 'blog/news_by_tag.html', context)
