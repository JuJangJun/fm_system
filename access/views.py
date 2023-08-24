from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, F, ExpressionWrapper, IntegerField
from django.utils.timezone import now

from .models import *
from pOCR import OCRmodel
import re
from datetime import datetime, date
from attend.models import Workers
# Create your views here.



#### 위험 지역 입출력 함수 ####
ocr_model2 = OCRmodel()  # 모델 로드
img = r"C:\Users\Playdata\Desktop\gungseo\501.png"
today = date.today()  # today 날짜 출력

def access_inout(request):
    ################################################# 어느 구역에 들어가는지 처리 나중에 구현 #################################################
    pid = Place.objects.get(p_id='A100')

    # 0. ocr 모델 실행 > return wid
    text, _ = ocr_model2.recognize(img)
    wid = re.findall('\d+', text[0])  # 정규표현식으로 숫자만 뽑음    
    
    # 1. access 테이블에 in_time = today, w_id = wid 확인
    try:
        worker = Workers.objects.get(w_id = wid[0])  # Workers에서 w_id 값이 wid[0]인 객체 추출
        existing_access = Access.objects.filter(w_id = worker, in_time__date = today, p_id = pid)  # 오늘 날짜, 위험 구역, 해당 작업자 in 기록 확인
        # <QuerySet [<Access: Access object (1)>, <Access: Access object (2)>]> 반환
        # 없으면 빈 쿼리셋 반환

        ## 1) 위험구역 안에 wid 기록이 있는 경우
        if existing_access.exists():
            print(wid[0], pid, '>> 안에 있음')
            last_access = existing_access.last()  # 이 사람의 마지막 access 조회 

            ### (1) out_time 없는 경우 out_time = now
            if not last_access.out_time:
                last_access.out_time = datetime.now()
                last_access.save()
                print(f'{wid[0]}, {pid}, in_time = {last_access.in_time.strftime("%Y-%m-%d %H:%M:%S")} >>> 현재 위험 구역 벗어남!')
                return render(request, 'access/access.html', 
                            {'wid_in' : wid[0], 'msg1': f'{pid} 구역 IN == {last_access.in_time.strftime("%Y-%m-%d %H:%M:%S")}',
                            'wid_out': wid[0], 'msg2': f'{pid} 구역 OUT == {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'})
            
            ### (2) out_time 있는 경우 access 테이블에 데이터 입력 in_time = now, w_id = wid 데이터 입력
            else:  
                print(f'{wid[0]} >> 또 들어옴')
                access = Access.objects.create(w_id = worker, p_id = pid)
                return render(request, 'access/access.html', {'wid_in': wid[0], 'msg1': f'{pid} 구역 IN == {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'})
        
        ## 2) 위험 구역 안에 없는 경우 > access 테이블에 데이터 입력, w_id = wid
        else:
            access = Access.objects.create(w_id = worker, p_id = pid)
            print(wid[0], '>> 위험 구역 들어감')
            return render(request, 'access/access.html', {'wid_in': wid[0], 'msg1': f'{pid} 구역 IN == {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'})
        
    except Workers.DoesNotExist:
        print(wid[0], '>> 존재하지 않는 아이디')
        return render(request, 'attend/attend.html', {'wid': '', 'confidence': '', 'msg': wid[0]+' => 존재하지 않는 작업자 아이디입니다.'})



@api_view(['GET'])
#### 위험 지역 정보 출력 함수 ####
def getDatas(request):
    result = check_nums()
    print(result)
    return render(request, 'access/place_info.html', {'datas': result})  # 결과 출력


#### 위험 지역 인원수 파악 함수 ####
def check_nums():
    # 필터 적용 및 어그리게이션
    queryset = (
        Place.objects
        .filter(access__out_time__isnull=True, access__in_time__date=today)
        .annotate(현재_인원수=Count('access'),)
        .order_by('p_id')  # group by 대신 order_by 사용
    )

    # Select 원하는 필드 값
    result = queryset.annotate(
        미달_인원 = ExpressionWrapper(F('p_num') - F('현재_인원수'), output_field=IntegerField())
    ).values(
        'p_id', 'task_location', '위험도', 'p_num',
        구역코드=F('p_id'),
        구역_위치=F('task_location'),
        현재_인원수=F('현재_인원수'),
        위험도=F('danger_degree'),
        기준_인원=F('p_num'),
        미달_인원=F('미달_인원'),
    )

    return result
