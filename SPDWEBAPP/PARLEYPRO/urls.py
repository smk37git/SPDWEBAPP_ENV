from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.change_vote, name="poll"),

    #path('logout/', views.logoutUser, name="logout"),
]
