from django.shortcuts import render
from rest_framework.decorators import api_view
from django.db.models import Count, F, ExpressionWrapper, IntegerField, Case, When

from .models import *
from pOCR import OCRmodel
import re
from datetime import datetime, date
from attend.models import Workers
from django.utils import timezone

import urllib.request
import cv2
import numpy as np
import time

######################## 경고메시지 전송 관련 
import requests
import json
from attend.views import ocr_model1

#### 위험 지역 입출력 함수 ####
# ocr_model2 = OCRmodel()  # 모델 로드
# img = r"C:\Users\Playdata\Desktop\gungseo\419.png"

url='http://192.168.0.5:8080/shot.jpg'
today = date.today()  # today 날짜

def access_inout(request):
    result = getDatas()  # 작업구역 정보 뽑아오기 
    pid = Place.objects.get(p_id='A100')
    
    #### (실시간) OCR 모델 recognize 실행
    while True:
        try:  # url(ip webcam)연결 오류 처리
            imgResp = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            print(f"!! ERROR !! IP_webcam 연결 상태를 확인하시오: {e}")
            return render(request, 'attend/error.html')
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp,-1)  
        
        # 이미지 사이즈 줄이기
        img = cv2.resize(img, (720 , 486), interpolation=cv2.INTER_AREA)
        
        # OCR 실행 
        time.sleep(1)
        text, _ = ocr_model1.recognize(img)
        try:  # 아무것도 못 찾았을 때 대비
            wid = re.findall('\d+', text[0])
            # 1. access 테이블에 in_time = today, w_id = wid 확인
            try:
                worker = Workers.objects.get(w_id = wid[0])  # Workers에서 w_id 값이 wid[0]인 객체 추출
                existing_access = Access.objects.filter(w_id = worker, in_time__date = today, p_id = pid)  # 오늘 날짜, 위험 구역, 해당 작업자 in 기록 확인
                # 없으면 빈 쿼리셋 반환
                
                ## 1) 위험구역 안에 wid 기록이 있는 경우
                if existing_access.exists():
                    print(wid[0], pid, '>> access 기록 있음')
                    last_access = existing_access.last()  # 이 사람의 마지막 access 조회 

                    ### (1) out_time 없는 경우 out_time = now
                    if not last_access.out_time:
                        elapsed_minutes = (datetime.now() - last_access.in_time.replace(tzinfo=None)).total_seconds() / 60

                        if elapsed_minutes < 1:  ## 다시 입력된 시간이 1분 미만인 경우 
                            print(f'{wid[0]}, {pid}, in_time={last_access.in_time.strftime("%Y-%m-%d %H:%M:%S")} >>>  들어온 지 아직 1분 미만!!!')
                            return render(request, 'access/workArea.html', 
                                        {'wid_in': wid[0], 'msg1': f'{last_access.in_time.strftime("%Y-%m-%d %H:%M")}','wid_out': '', 'msg2': '들어온 지 1분 미만',
                                        'datas':result})
                        
                        last_access.out_time = datetime.now()
                        last_access.save()

                        print(f'{wid[0]}, {pid}, in_time = {last_access.in_time.strftime("%Y-%m-%d %H:%M:%S")} >>> 현재 위험 구역 벗어남!')
                        return render(request, 'access/workArea.html', 
                                    {'wid_in' : wid[0], 'msg1': f'{last_access.in_time.strftime("%Y-%m-%d %H:%M")}',
                                    'wid_out': wid[0], 'msg2': f'{datetime.now().strftime("%Y-%m-%d %H:%M")}',
                                    'datas':result})
                    
                    ### (2) out_time 있는 경우 access 테이블에 데이터 입력 in_time = now, w_id = wid 데이터 입력
                    else:  
                        print(f'{wid[0]} >> 위험구역 n번째 입장')
                        access = Access.objects.create(w_id = worker, p_id = pid)
                        return render(request, 'access/workArea.html', {'wid_in': wid[0], 'msg1': f'{datetime.now().strftime("%Y-%m-%d %H:%M")}'
                                                                        ,'datas':result})
                
                ## 2) 위험 구역 안에 없는 경우 > access 테이블에 데이터 입력, w_id = wid
                else:
                    access = Access.objects.create(w_id = worker, p_id = pid)
                    print(wid[0], '>> 위험 구역 첫입장')
                    return render(request, 'access/workArea.html', {'wid_in': wid[0], 'msg1': f'{datetime.now().strftime("%Y-%m-%d %H:%M")}','datas':result})
                
            except Workers.DoesNotExist:
                print(wid[0], '>> 존재하지 않는 아이디')
                return render(request, 'access/workArea.html', {'wid': '', 'confidence': '', 'msg': wid[0]+' | Wrong ID','datas':result})

        except Exception as e:
            print('access - 아무 텍스트도 인식하지 못함')
            return render(request, 'access/workArea.html', {'datas':result, 'msg':'NO TEXT'})


# @api_view(['GET'])
#### 위험 지역 정보 출력 함수 ####
def getDatas():
    result = check_nums()
    print(result)
    # return render(request, 'access/workArea.html', {'datas': result})  # 결과 출력
    return result



##############################################################################################################################################################################
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
    미달_인원=Case(
            When(현재_인원수__lte=F('p_num'), then=F('p_num') - F('현재_인원수')),
            default=0,
            output_field=IntegerField()
        )
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



####################################################################################
# 경고메시지 전송 관련 
def send_slack_message(message):
    webhook_url = 'https://hooks.slack.com/services/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'  # 생성한 Webhook URL
    slack_data = {'text': message}
    
    response = requests.post(
        webhook_url,
        data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200:
        raise ValueError(
            f'Request to slack returned an error {response.status_code}',
            f'the response is:\n{response.text}')
####################################################################################


#### 기준 인원 미달일 경우 slack에 데이터 저장 함수 ####
import logging
logger = logging.getLogger(__name__)

def check_and_save_to_slack():
    # 위험 지역 인원수 파악
    result = check_nums()
    logger.info('check_and_save_to_slack 함수 실행 !!', datetime.now())
    
    # 각 구역에 대해 현재 인원수가 1명 이상이고 기준 인원 미달인 경우, Slack 테이블에 데이터 저장
    for place in result:
        if place['현재_인원수'] >= 1 and place['미달_인원'] > 0:
            msg = f"{place['구역_위치']}는 현재 {place['현재_인원수']}명이 있으며, {place['미달_인원']}명 더 필요합니다."
            logger.info('='*50)
            logger.info(msg)
            
            # 현재 날짜/시간 추출
            now = timezone.now()
            current_date_time = now.replace(second=0, microsecond=0)

            slack_message = Slack.objects.create(
                msg = msg,
                p_id = Place.objects.get(p_id=place['p_id']),
            )
            
            send_slack_message(msg)  # DB에 저장 후 경고 메시지 전송

        else:
            logger.info('========== 작업 구역 이상 없음 ==========')
