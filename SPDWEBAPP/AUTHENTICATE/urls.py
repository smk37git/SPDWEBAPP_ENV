from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # User Registration Paths
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('codeofethics/', views.codeOfEthics, name="codeOfEthics"),
    path('rush/', views.rush, name="rush"),
    path('roster/', views.roster, name="roster"),
    path('logout/', views.logoutUser, name="logout"),
]
