from django.urls import path
from . import views

app_name = 'opportunities'  #namespace for the app


urlpatterns = [
    path('opportunities/', views.opportunities, name='opportunities'),
    path('createOpportunity/', views.createOpportunity, name='createOpportunity'),
]