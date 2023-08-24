from django.urls import path
from . import views

urlpatterns = [
    # path('', views.getTestDatas, name="visualization"),
    path('', views.model_view, name='index'),  # 수연
    path('statistics/', views.getViewsDatas, name="statistics"),
]