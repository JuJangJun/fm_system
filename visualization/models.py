from django.db import models


## 경고 코드 관련 정보를 담은 테이블
class Codes(models.Model):
    code = models.CharField(max_length=20, primary_key=True)  # 경고 코드
    content = models.CharField(max_length=50, null=False)  # 경고 내용


#### 월별 보호구 코드별 인원수 조회 뷰 ####
class MonthSafetyCntView(models.Model):
    id = models.AutoField(primary_key=True)  # id 필드 추가
    month = models.IntegerField()
    code = models.CharField(max_length=20)
    code_count = models.IntegerField()
    content= models.CharField(max_length=50) 

    class Meta:
        managed=False 
        db_table='new_month_safetycnt_view' 


#### 월, 일별 보호구 착용 인원수 확인 뷰 (N, 그 외) ####
class NormalSFView(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    day = models.IntegerField()
    normal_cnt = models.IntegerField()
    unnormal_cnt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'normal_sf_view'


#### 월별 보호구 HGV별 인원수 조회 뷰 ####
class HgvCntView(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    helmet = models.IntegerField()
    goggle = models.IntegerField()
    vest = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hgv_cnt_view'
