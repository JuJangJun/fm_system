from django.db import models
from django.utils import timezone
from datetime import datetime
from attend.models import Workers


## 작업 구역에 관한 정보를 저장하는 테이블
class Place(models.Model):
    p_id = models.CharField(max_length=10, primary_key=True)  # 구역 아이디
    task_location = models.CharField(max_length=50, null=False)  # 작업 위치
    danger_degree = models.PositiveIntegerField(null=False)  # 위험도
    p_num = models.PositiveIntegerField(null=False)  # 기준 인원


## 각 구역 출입 정보를 담은 테이블
class Access(models.Model):
    a_id = models.AutoField(primary_key=True)  # 출입 아이디
    w_id = models.ForeignKey(Workers, on_delete=models.CASCADE)  # 작업자 아이디 (외래키)
    p_id = models.ForeignKey(Place, on_delete=models.CASCADE)  # 구역 아이디 (외래키)
    in_time = models.DateTimeField(default=datetime.now, blank=True) # 출입 시간
    out_time = models.DateTimeField(null=True)  # 나간 시간


## 구역 경고 관련 슬랙 메시지 저장 테이블
class Slack(models.Model):
    slack_id = models.AutoField(primary_key=True)  # 식별 아이디
    msg = models.CharField(max_length=100, null=True)  # 경고 메시지
    p_id = models.ForeignKey(Place, on_delete=models.CASCADE)  # 구역 아이디 (외래키)
    slack_time = models.DateTimeField(default=datetime.now, blank=True)  # 경고 날짜/시간