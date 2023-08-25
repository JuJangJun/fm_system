from django.shortcuts import render, redirect
from .forms import WorkersForm
from pOCR import OCRmodel
from .ip_webcam_paddleOCR import Webcam

from django.db import connection
from .models import *
import re
from datetime import datetime, date


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


#### OCR 모델 돌리고 결과 화면에 출력 & 디비 저장 함수 ####
ocr_model1 = OCRmodel()  # 모델 로드
img = r"C:\Users\Playdata\Desktop\gungseo\419.png"

## 출근 ##
def check_attendance(request):
    # ocr 모델 recognize 실행
    # text, confidence = Webcam()
    text, confidence = ocr_model1.recognize()
    wid = re.findall('\d+', text[0])  # 정규표현식으로 숫자만 뽑음

    # today 날짜 출력
    today = date.today()
    print('='*50, '\n오늘 날짜:', today)

    ## wid가 workers 테이블에 존재하면, 출석부에 작업자 출근 정보 입력
    try:
        worker = Workers.objects.get(w_id = wid[0])  # Workers에서 작업자 정보 추출
        existing_attendance = Attendance.objects.filter(w_id = worker, attend_time__date = today)  # 오늘 날짜, 해당 작업자 출근 기록 확인
        
        if existing_attendance.exists():
            print(wid[0], '>> 이미 출근한 기록이 있습니다.')
            return render(request, 'attend/webcam.html', {'wid': '', 'confidence': '', 'msg': wid[0]+' => 이미 출근한 기록이 있습니다.'})
        
        else:
            attendance = Attendance.objects.create(w_id = worker)
            print(wid[0], '>> 출근 입력 완료')
            check = safety_chk(worker, attendance)  # detection 모델 + db 저장 함수
            return render(request, 'attend/webcam.html', {'wid': wid[0], 'confidence': confidence[0], 'msg': wid[0]+' => 출근 기록 완료!', 'code':check})
        
    except Workers.DoesNotExist:
        print(wid[0], '>> 존재하지 않는 아이디')
        return render(request, 'attend/webcam.html', {'wid': '', 'confidence': '', 'msg': wid[0]+' => 존재하지 않는 작업자 아이디입니다.'})


## 퇴근 ## 
def check_leave(request):
    # OCR 모델 recognize 실행
    # text, confidence = Webcam()
    text, confidence = ocr_model1.recognize()
    wid = re.findall('\d+', text[0])  # 정규표현식으로 숫자만 뽑음
    today = date.today()  # today 날짜 출력

    try:  
        # 해당 작업자의 퇴근 기록 유무 확인
        attendance_data = Attendance.objects.get(attend_time__date=today, w_id=wid[0])

        # 퇴근 시간을 미등록한 경우, 현재 시간으로 업데이트
        if not attendance_data.leave_time:
            attendance_data.leave_time = datetime.now()
            attendance_data.save()
            print(f'{wid[0]} >> 퇴근 기록 완료!')
            return render(request, 'attend/leave.html', {'wid': wid[0], 'confidence': confidence[0], 'msg': f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {wid[0]} 퇴근 기록'})
        
        # 이미 퇴근 완료한 경우
        else:  
            print(f'{wid[0]} >> 이미 퇴근 완료함')
            return render(request, 'attend/leave.html', {'wid': '', 'confidence': '', 'msg': f'{wid[0]} 이미 퇴근 완료하였습니다.'})

    except Attendance.DoesNotExist:
        # 출근하지 않은 작업자인 경우
        print(f'Attendance Error == {wid[0]}, 출근하지 않은/없는 작업자 입니다.')
        return render(request, 'attend/leave.html', {'wid': '', 'confidence': '', 'msg': f'{wid[0]} 출근하지 않은/없는 작업자 입니다.'})


#### Safety_check 테이블 입력 함수 - 입력: worker, attendance ####
def safety_chk(worker, attendance):
    ### detection 모델 작동 > 결과 출력: RESULT ###
    result = 'G' # 전원 미착용

    # Safety_check 데이터 입력(외래키 att_id, w_id)
    safetycheck = Safety_check.objects.create(w_id = worker, att_id=attendance, sc_code=result)
    print(worker, attendance, result)

    return result