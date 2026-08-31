from django.urls import path
from . import views


urlpatterns = [
    path('', views.sober_sheet_dashboard, name='sober_sheet_dashboard'),
    path('request/', views.sober_sheet_request, name='sober_sheet_request'),
    path('approve/', views.sober_sheet_approve, name='sober_sheet_approve'),
]
