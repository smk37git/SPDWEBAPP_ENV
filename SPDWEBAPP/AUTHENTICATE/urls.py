from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # User Registration Paths
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('ourhistory/', views.ourHistory, name="ourHistory"),
    path('codeofethics/', views.codeOfEthics, name="codeOfEthics"),
    path('rush/', views.rush, name="rush"),
    path('roster/', views.roster, name="roster"),
    path('logout/', views.logoutUser, name="logout"),
    path('change-password/', views.change_password, name='change-password'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_photo/', views.update_photo, name='update_photo'),
    path('reset-photo/', views.reset_photo, name='reset_photo'),
    path('update_majors/', views.update_majors, name='update_majors'),
    path('add-custom-major/', views.add_custom_major, name='add_custom_major'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
