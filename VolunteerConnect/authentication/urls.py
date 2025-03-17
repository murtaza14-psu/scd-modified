from django.urls import path
from . import views

app_name = 'authentication'  # Namespace for the app

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
]