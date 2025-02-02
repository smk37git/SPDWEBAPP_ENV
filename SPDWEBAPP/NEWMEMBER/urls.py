from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.newmember_dashboard, name="newmember_dashboard"),
    path('marks/', views.newmember_marks_dashboard, name="newmember_marks_dashboard"),
    path('request/', views.newmember_request, name="newmember_request"),
    path('approve/', views.newmember_approve, name="newmember_approve"),
     path('history/<int:user_id>/', views.newmember_mark_history, name='newmember_mark_history'),
]
