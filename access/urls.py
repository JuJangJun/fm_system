from django.urls import path
from . import views

urlpatterns = [
    path('', views.access_inout, name='user-workarea'),  # getDatas랑 같이 뿌리기 시도 
]
