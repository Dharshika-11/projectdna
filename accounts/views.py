from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import User, UserProfile, Department

def register_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, f"Welcome to PROJECTDNA NEXUS, {user.username}! Your account was created successfully.")
                return redirect(user.get_dashboard_url())
            except Exception as e:
                messages.error(request, "Registration failed: A user with this Roll Number or Username already exists.")
        else:
            messages.error(request, "Registration failed. Please review the errors below.")
    else:
        form = CustomUserCreationForm()
    
    departments = Department.objects.all()
    return render(request, 'accounts/register.html', {'form': form, 'departments': departments})

def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(user.get_dashboard_url())
        messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('core:landing')

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()

        if p_form.is_valid():
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
    else:
        p_form = ProfileUpdateForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
        })

    return render(request, 'accounts/profile.html', {'p_form': p_form, 'profile': profile})
