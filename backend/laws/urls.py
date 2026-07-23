"""
URLs for law and article pages related to cyber crimes.
"""
from django.urls import path
from . import views

app_name = 'laws'

urlpatterns = [
    path('', views.law_index_view, name='law_index'),
    path('<str:category>/', views.law_detail_view, name='law_detail'),
]
