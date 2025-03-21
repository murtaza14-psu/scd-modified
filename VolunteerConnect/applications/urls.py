from django.urls import path
from . import views
app_name = 'applications'  #namespace for the app

urlpatterns = [
    path('apply/<int:opportunity_id>/', views.apply_opportunity, name='apply_opportunity'),
    path('manage/<int:opportunity_id>/', views.manage_opportunity, name='manage_opportunity'),
    path('check-in/<int:opportunity_id>/<int:volunteer_id>/', views.check_in, name='check_in'),
    path('check-out/<int:attendance_id>/', views.check_out, name='check_out'),
    path('export-attendance/<int:opportunity_id>/', views.export_attendance_excel, name='export_attendance_excel'),
]