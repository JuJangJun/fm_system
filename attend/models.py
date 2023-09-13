from django.db import models
from django.utils import timezone
from datetime import datetime

## 작업자들의 정보를 담은 테이블
class Workers(models.Model):
    w_id = models.PositiveIntegerField(primary_key=True)  # 작업자 아이디
    wname = models.CharField(max_length=50, null=False)  # 작업자 이름
    manager_id = models.PositiveIntegerField(null=True)  # 담당자 아이디
    contact = models.CharField(max_length=20, null=False)  # 작업자 연락처
    email = models.EmailField(null=True)  # 작업자 이메일


## 출퇴근 날짜/시간 데이터를 저장할 테이블
class Attendance(models.Model):
    att_id = models.AutoField(primary_key=True)  # 출석부 아이디
    w_id = models.ForeignKey(Workers, on_delete=models.CASCADE)  # 작업자 아이디 (외래키)
    attend_time = models.DateTimeField(default=datetime.now, blank=True) # 출근 날짜/시간
    leave_time = models.DateTimeField(null=True)  # 퇴근 날짜/시간


## 보호구 착용 여부를 저장할 테이블
class Safety_check(models.Model):
    sc_id = models.AutoField(primary_key=True)  # 식별 아이디
    sc_code = models.CharField(max_length=20, null=False)  # 경고 코드
    att_id = models.ForeignKey(Attendance, on_delete=models.CASCADE) # 출석부 아이디 (외래키)
    w_id = models.ForeignKey(Workers, on_delete=models.CASCADE)  # 경고를 받은 작업자 아이디 (외래키)



