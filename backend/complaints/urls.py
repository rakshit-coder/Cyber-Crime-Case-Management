"""
URL configuration for Complaints application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaints_list_view, name='complaints_list'),
    path('new/', views.new_complaint_view, name='new_complaint'),
    path('<str:case_number>/', views.complaint_detail_view, name='complaint_detail'),
    path('<str:case_number>/legal-info/', views.complaint_legal_info_view, name='complaint_legal_info'),
    path('<str:case_number>/upload-evidence/', views.upload_evidence_view, name='upload_evidence'),
    path('<str:case_number>/approve/', views.approve_complaint_view, name='approve_complaint'),
    path('<str:case_number>/reject/', views.reject_complaint_view, name='reject_complaint'),
    path('<str:case_number>/download-pdf/', views.download_complaint_pdf, name='download_complaint_pdf'),
    path('api/pending-complaints/', views.get_pending_complaints_api, name='pending_complaints_api'),
]
