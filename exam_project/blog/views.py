from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from exam_project.blog.models import Post, Category, Tag, Comment
from .forms import CommentForm
from ..shop.models import Product


def get_categories():
    try:
        return Category.objects.all()
    except Category.DoesNotExist:
        return None


def home_page(request):

    latest_post = Post.objects.last()
    posts = Post.objects.order_by('-created_at')[1:4]
    categories = get_categories()

    latest_products = Product.objects.order_by('-id')[:4]

    context = {
        'latest_post': latest_post,
        'posts': posts,
        'categories': categories,
        'latest_products': latest_products,

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


@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    else:
        # Redirect to some error page or show an error message
        return HttpResponse("You don't have permission to delete this comment.")


@login_required
def edit_comment(request, post_pk, comment_pk):
    categories = get_categories()
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        return HttpResponseForbidden("You don't have permission to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Save the changes to the existing comment
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'post': post,
        'form': form,
        'categories': categories,
    }

    return render(request, 'blog/edit-comment.html', context)

