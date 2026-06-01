from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import EditProfileForm, EmailAuthenticationForm, SignUpForm, StyledPasswordChangeForm


def _safe_next_url(request, fallback='home'):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    return reverse(fallback)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = EmailAuthenticationForm(request=request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if form.cleaned_data.get('remember_me'):
            request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            request.session.set_expiry(0)
        user.mark_seen()
        messages.success(request, 'Welcome back. You are logged in.')
        return redirect(_safe_next_url(request, 'home'))

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        user.mark_seen()
        messages.success(request, 'Your account has been created. You are logged in.')
        return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile_view(request):
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your profile was updated.')
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = StyledPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was changed.')
        return redirect('profile')
    return render(request, 'accounts/change_password.html', {'form': form})
