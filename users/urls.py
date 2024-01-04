from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_reset/', views.password_change, name='password_reset'),
    path('index/', views.index, name='index')

]
