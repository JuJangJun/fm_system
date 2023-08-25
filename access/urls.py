from django.urls import path
from . import views

urlpatterns = [
    # path('', views.access_inout, name='access_inout'),  # 위험구역 들어갔다 나왔다    
    path('inout/', views.access_inout, name='access_inout'),
    path('', views.getDatas, name='user-workarea'),  # 구역 정보 확인 페이지
    
]
