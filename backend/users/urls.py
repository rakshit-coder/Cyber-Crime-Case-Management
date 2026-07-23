"""
URL configuration for Users application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('set-new-password/', views.set_new_password_view, name='set_new_password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    path('force-reset-password/', views.force_password_reset_view, name='force_reset_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('cyber-awareness/', views.cyber_awareness_view, name='cyber_awareness'),
    path('set-language/', views.set_language_view, name='set_language'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', views.manage_users_view, name='manage_users'),
    path('admin/users/add/', views.add_user_view, name='add_user'),
    path('admin/users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('admin/users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/officers/', views.manage_officers_view, name='manage_officers'),
    path('admin/officers/add/', views.add_officer_view, name='add_officer'),
    path('admin/officers/<int:officer_id>/edit/', views.edit_officer_view, name='edit_officer'),
    path('admin/cases/', views.admin_cases_view, name='admin_cases'),
    path('admin/email-settings/', views.email_settings_view, name='email_settings'),
    path('admin/email-settings/test/', views.send_test_email_view, name='send_test_email'),
]
