from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.urls import reverse

from .forms import UserRegistrationForm, UserEditForm, UserProfileForm
from .models import CustomUser
from .. import settings


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/../../templates/user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Проверка дали потребителя е персонал от администрацията
            if user.is_staff:
                # Установяване на бисквитка за сесия в администрацията
                response = HttpResponseRedirect(reverse('admin:index'))
                response.set_cookie(settings.ADMIN_SESSION_COOKIE_NAME, value='admin_session_value')
                return response
            else:
                return redirect('profile')
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'user/login.html')


@login_required
def profile(request):
    return render(request, 'user/profile.html')


def user_logout_view(request):
    user_logout(request)
    # Премахване на бисквитката за сесия в администрацията
    response = redirect('home')
    response.delete_cookie(settings.ADMIN_SESSION_COOKIE_NAME)
    return response


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'user/delete_profile.html')

