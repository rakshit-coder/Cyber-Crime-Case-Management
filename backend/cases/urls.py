"""
URL configuration for Cases application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases_list_view, name='cases_list'),
    path('<str:case_number>/report/', views.case_report_view, name='case_report'),
    path('dashboard/', views.dashboard_view, name='cases_dashboard'),
    path('unassigned/', views.unassigned_cases_view, name='unassigned_cases'),
    path('api/assign/', views.assign_case_to_officer, name='assign_case'),
    path('api/update-status/', views.update_case_status, name='update_case_status'),
]
