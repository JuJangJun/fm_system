from django.shortcuts import render, redirect
from .forms import WorkersForm
from pOCR import OCRmodel
# from .ip_webcam_paddleOCR import Webcam

from django.db import connection
from .models import *
import re
from datetime import datetime, date

import urllib.request
import cv2
import numpy as np
import time

## 경준오빠 파일 import
from .ip_cam import IpCam 
url='http://192.168.0.5:8080/shot.jpg'

# today 날짜 출력
today = date.today()
print('='*50, '\n오늘 날짜:', today)


#################################################################################################################################
#### OCR 모델 돌리고 결과 화면에 출력 & 디비 저장 함수 ####
ocr_model1 = OCRmodel()  # 모델 생성

## 출근 ##
def check_attendance(request):

    #### (실시간) ocr 모델 recognize 실행
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
        try:
            wid = re.findall('\d+', text[0])
            try:
                worker = Workers.objects.get(w_id = wid[0])  
                # existing_attendance 작업자 존재하는지 확인
                existing_attendance = Attendance.objects.filter(w_id = worker, attend_time__date = today)  # 오늘 날짜, 해당 작업자 출근 기록 확인
                
                if existing_attendance.exists():
                    print(wid[0], '>> 이미 출근한 기록이 있습니다.')
                    ## safety_check 테이블에 att_id가 없는 경우 다시 보호구 착용 확인
                    try:
                        existing_sc = Safety_check.objects.get(att_id=existing_attendance.first())
                        print('safety_check 있음')
                        return render(request, 'attend/webcam.html', {'wid': wid[0], 'wname': worker.wname, 'code':existing_sc.sc_code, 'msg':'출근 기록 있음'})
                    
                    except Safety_check.DoesNotExist:
                        print(f'!! ERROR !! {wid[0]} >> safety_check 다시 실행 !!')
                        check_result = safety_chk(worker, existing_attendance.first(), url)   
                        # check_result = safety_chk.delay(worker.id, attendance.id, url)  ## delay는 celery 태스크를 비동기적으로 실행하도록 예약
                        return render(request, 'attend/webcam.html', {'wid': wid[0], 'wname': worker.wname, 'code':check_result['wc'], 'msg':'안전구 확인 완료'})
                
                else:
                    attendance = Attendance.objects.create(w_id = worker)
                    print(f'{wid[0]} >> 출근 입력 완료')
                    check = safety_chk(worker, attendance, url)  
                    # check = safety_chk.delay(worker.id, attendance.id, url)
                    return render(request, 'attend/webcam.html', {'wid': wid[0], 'wname': worker.wname, 'code':check['wc'], 'msg': '출근, 안전구 확인 완료'})
                
            except Workers.DoesNotExist:
                print(f'!! ERROR !! {wid[0]} >> 존재하지 않는 아이디')
                return render(request, 'attend/webcam.html', {'msg': wid[0]+' | Wrong ID'})
        
        except Exception as e:
            print(f'!! ERROR !! attend - 아무 텍스트도 인식하지 못함 or {e}')
            return render(request, 'attend/webcam.html', {'msg':'No TEXT'})


def safety_chk(worker, attendance, url):
    result = IpCam.cam_2(url)  # {"wc" : warning_code, "wr" : wear}
    print("result : ",result)
    wc = result['wc']

    # Safety_check 데이터 입력(외래키 att_id, w_id)
    safetycheck = Safety_check.objects.create(w_id = worker, att_id=attendance, sc_code=wc)
    print(worker, attendance, wc)

    return result


############# ajax 이용 비동기 작업 확인 ####################################################################################################################
# from django.http import JsonResponse

# def get_status(request):
#     if is_ready():
#         return JsonResponse({'status': 'ready', 'result': check_attendance()})
#     else:
#         return JsonResponse({'status': 'not_ready'})


#################################################################################################################################
## 퇴근 ## 
def check_leave(request):

    #### (실시간) ocr 모델 recognize 실행
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
        text, _ = ocr_model1.recognize(img)
        try:  # 아무것도 못 찾았을 때 대비
            wid = re.findall('\d+', text[0])
            try:  
                # 해당 작업자의 퇴근 기록 유무 확인
                attendance_data = Attendance.objects.get(attend_time__date=today, w_id=wid[0])
                worker = Workers.objects.get(w_id = wid[0])  # Workers에서 작업자 정보 추출

                # 퇴근 시간을 미등록한 경우, 현재 시간으로 업데이트
                if not attendance_data.leave_time:
                    attendance_data.leave_time = datetime.now()
                    attendance_data.save()
                    print(f'{wid[0]} >> 퇴근 기록 완료!')
                    return render(request, 'attend/leave.html', {'wid': wid[0], 'wname': worker.wname, 'msg': '퇴근 기록 완료'})
                
                # 이미 퇴근 완료한 경우
                else:  
                    print(f'{wid[0]} >> 이미 퇴근 완료함')
                    return render(request, 'attend/leave.html', {'wid': wid[0], 'wname': worker.wname, 'msg': '퇴근 기록 있음'})

            except Attendance.DoesNotExist:
                # 출근하지 않은 작업자인 경우
                print(f'Attendance Error == {wid[0]}, 출근하지 않은/없는 작업자 입니다.')
                return render(request, 'attend/leave.html', {'msg': f'{wid[0]} | Wrong ID'})
            
        except Exception as e:
            print('leave - 아무 텍스트도 인식하지 못함')
            return render(request, 'attend/leave.html', {'msg':'No TEXT'})


#################################################################################################################################
#### mySQL DB 연결 ####
def connect_db():
    cursor = connection.cursor()
    return cursor


#### workers 작업자 추가 폼 ####
def create_worker(request):
    if request.method == 'POST':
        form = WorkersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = WorkersForm()

    return render(request, 'attend/create_worker.html', {'form': form})