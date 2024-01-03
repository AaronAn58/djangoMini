from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自动登录用户
            return redirect('/')  # 根据需要重定向到其他页面
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def logout(request):
    return render(request, 'index.html')


def password_change(request):
    return render(request, 'login/password_change_form.html')
