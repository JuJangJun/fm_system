from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Codes, MonthSafetyCntView, NormalSFView, HgvCntView

from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .dash import app


# @api_view - 데코레이션. get 메소드 사용
# @api_view(['GET'])
# def getTestDatas(request):
#     datas = Codes.objects.all()  # Codes 테이블에 있는 데이터 모두를 읽어들임
#     return render(request, 'visualization/visualization.html', {'datas':datas})  # 결과 출력


#### 월, 일별 보호구 착용 인원수 확인 뷰 (N, 그 외) 조회 ####
#### 월별 보호구 HGV별 인원수 조회 뷰 ####
@api_view(['GET'])
def getViewsDatas(request):
    views1 = NormalSFView.objects.all() 
    views2 = HgvCntView.objects.all() 
    return render(request, 'visualization/statistics_base.html', {'views1': views1, 'views2':views2})


def model_view(request):
    return render(request, "visualization/statistics.html")