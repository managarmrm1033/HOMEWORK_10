from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm
from .forms import ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


def signupuser(request):
    if request.user.is_authenticated:
        return redirect('noteapp:main')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматично входить після реєстрації
            return redirect('noteapp:main')
        else:
            messages.error(request, 'Error during registration')
            return render(request, 'users/signup.html', {'form': form})

    return render(request, 'users/signup.html', {'form': UserCreationForm()})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('noteapp:main')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('noteapp:main')  # Перенаправлення після успішного входу
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('users:login')

    return render(request, 'users/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='noteapp:main')

@login_required
def profile(request):
    # Якщо профіль не існує, створюємо його
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('users:profile')

    profile_form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('noteapp:note')  # перенаправлення після успішного входу
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})