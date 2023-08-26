from django.urls import path
from . import views

urlpatterns = [
    # path('test/', views.getTestDatas, name="visualization"),
    path('', views.model_view, name='user-statistics'),  # 수연
    path('views/', views.getViewsDatas, name="views"),
]