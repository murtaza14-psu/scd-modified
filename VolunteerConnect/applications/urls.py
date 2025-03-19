from django.urls import path
from . import views
app_name = 'applications'  #namespace for the app

urlpatterns = [
    path('apply/<int:opportunity_id>/', views.apply_opportunity, name='apply_opportunity'),
    path('manage/<int:opportunity_id>/', views.manage_opportunity, name='manage_opportunity'),
]