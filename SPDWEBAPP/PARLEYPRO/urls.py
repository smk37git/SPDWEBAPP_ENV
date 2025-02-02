from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.poll_index, name="poll"),
    path('start_vote/',views.start_vote, name="start_vote"),
    path('past_polls/', views.past_polls, name='past_polls'),

]
