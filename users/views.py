from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('yolov8:video_list')  # Redirect to the home page or another desired page
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def logout(request):
    return render(request, 'index.html')


def password_change(request):
    return render(request, 'login/password_change_form.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('yolov8:video_list')  # Redirect to the desired URL after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})
