from django.urls import path
from . import views


urlpatterns = [
    path('create_worker/', views.create_worker, name='create_worker'),  # 새로운 작업자 입력 폼
    path('', views.check_attendance, name='user-webcam'),  # 출석 확인 페이지
    path('leave/', views.check_leave, name='check_leave')  # 퇴근 확인 페이지
]
