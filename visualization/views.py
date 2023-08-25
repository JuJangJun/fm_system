from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Codes, MonthSafetyCntView

from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .dash import app


# @api_view - 데코레이션. get 메소드 사용
# @api_view(['GET'])
# def getTestDatas(request):
#     datas = Codes.objects.all()  # Codes 테이블에 있는 데이터 모두를 읽어들임
#     return render(request, 'visualization/visualization.html', {'datas':datas})  # 결과 출력


#### 월별 최초 통과 보호구 수 조회 ####
# @api_view(['GET'])
# def getViewsDatas(request):
#     views = MonthSafetyCntView.objects.all()  # Codes 테이블에 있는 데이터 모두를 읽어들임

#     for result in views:
#         print(result.month, result.code,result.code_count,result.content)

#     return render(request, 'visualization/statistics.html', {'views': views})


def model_view(request):
    return render(request, "visualization/statistics.html")