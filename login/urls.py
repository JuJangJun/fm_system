from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name = "user-dashboard"),
    path('', views.user_login, name='user-login'),
    path('register/', views.user_register, name='user-register'),
    path('logout/', views.user_logout, name='user-logout'),
]