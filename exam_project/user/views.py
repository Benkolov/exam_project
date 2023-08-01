from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout

from .forms import UserRegistrationForm, UserEditForm, UserProfileForm

from .. import settings

from ..blog.views import get_categories


def register(request):
    categories = get_categories()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'user/register.html', context)


def user_login(request):
    categories = get_categories()

    context = {
        'categories': categories,
    }

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')

        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'user/login.html', context)


@login_required
def profile(request):
    categories = get_categories()

    context = {'categories': categories}

    return render(request, 'user/profile.html', context)


@login_required()
def user_logout_view(request):
    user_logout(request)

    response = redirect('home')
    response.delete_cookie(settings.ADMIN_SESSION_COOKIE_NAME)
    return response


@login_required
def edit_profile(request):
    categories = get_categories()

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile) # change this line
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile) # and this line

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'categories': categories
    }

    return render(request, 'user/edit_profile.html', context)


@login_required
def delete_profile(request):
    categories = get_categories()
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')

    context = {
        'categories': categories
    }

    return render(request, 'user/delete_profile.html', context)
