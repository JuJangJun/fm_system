from django.urls import path
from . import views

urlpatterns = [
    path('', views.model_view, name='user-statistics'),  # 수연
]