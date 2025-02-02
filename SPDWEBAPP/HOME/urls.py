from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    path('ourhistory/', views.ourHistory, name="ourHistory"),
    path('codeofethics/', views.codeOfEthics, name="codeOfEthics"),
    path('rush/', views.rush, name="rush"),]