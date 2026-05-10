from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'home.html')

def signup_view(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.http import JsonResponse
from .models import User

def validate_email(request):
    email = request.GET.get('email', None)
    if email and User.objects.filter(email=email).exists():
        return JsonResponse({'is_taken': True})
    return JsonResponse({'is_taken': False})

def validate_username(request):
    username = request.GET.get('username', None)
    if username and User.objects.filter(username=username).exists():
        return JsonResponse({'is_taken': True})
    return JsonResponse({'is_taken': False})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm
from tasks.models import Task
from projects.models import Membership

@login_required
def profile_view(request):
    user = request.user
    
    total_projects = Membership.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(assignee=user, status='COMPLETED').count()
    pending_tasks = Task.objects.filter(assignee=user).exclude(status='COMPLETED').count()
    
    context = {
        'total_projects': total_projects,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        if 'update_account' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('settings')
        
        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        
    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'accounts/settings.html', context)

@login_required
def profile_setup(request):
    profile = request.user.profile
    if profile.is_setup_complete:
        return redirect('dashboard')
        
    if request.method == 'POST':
        display_name = request.POST.get('display_name', '').strip()
        role = request.POST.get('role', '').strip()
        
        if display_name:
            profile.display_name = display_name
            profile.role = role
            profile.is_setup_complete = True
            profile.save()
            return redirect('dashboard')
            
    return render(request, 'profile_setup.html')