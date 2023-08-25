from django.urls import path
from . import views

urlpatterns = [
    path('', views.access_inout, name='access_inout'),  # 위험구역 들어갔다 나왔다
    path('workArea/', views.getDatas, name='workArea')  # 구역 정보 확인 페이지
]
