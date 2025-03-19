# attendance/urls.py
from django.urls import path
from . import views

app_name = 'engagement'  #namespace for the app

urlpatterns = [
    path('manage/<int:opportunity_id>/', views.manage_attendance, name='manage_attendance'),
]