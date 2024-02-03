from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            signup_form = RegistrationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect('home')
        else:
            signup_form = RegistrationForm()
        return render(request, 'signup.html', {'form': signup_form})
    else:
        return redirect('profile')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid:
                user_name = request.POST.get('username')
                user_pass = request.POST.get('password')
                user = authenticate(username=user_name, password=user_pass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('profile')
                else:
                    return redirect('signup')
        else:
            login_form = AuthenticationForm()
        return render(request, 'login.html', {'form': login_form})

    else:
        return redirect('profile')


def user_logout(request):
    logout(request)
    # messages.success(request, 'Logged out successfully')
    return redirect('home')


def profile(request):
    return render(request, 'profile.html')


def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass_form = PasswordChangeForm(request.user, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
                return redirect('profile')

        else:
            pass_form = PasswordChangeForm(request.user)
        return render(request, 'password_change.html', {'form': pass_form, 'type': 'Change'})

    else:
        return redirect('signup')


def set_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass_form = SetPasswordForm(request.user, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password set successfully')
                return redirect('profile')

        else:
            pass_form = SetPasswordForm(request.user)
        return render(request, 'password_change.html', {'form': pass_form, 'type': 'Set'})

    else:
        return redirect('login')
