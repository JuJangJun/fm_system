from django.db import models


## 경고 코드 관련 정보를 담은 테이블
class Codes(models.Model):
    code = models.CharField(max_length=20, primary_key=True)  # 경고 코드
    content = models.CharField(max_length=50, null=False)  # 경고 내용


# #### 월별 보호구 코드별 인원수 조회 뷰 ####
class MonthSafetyCntView(models.Model):
    id = models.AutoField(primary_key=True)  # id 필드 추가
    month = models.IntegerField()
    code = models.CharField(max_length=20)
    code_count = models.IntegerField()
    content= models.CharField(max_length=50) # 추가된 필드

    class Meta:
        managed=False # This ensures that Django won't try to create a table for this model.
        db_table='new_month_safetycnt_view' # This is the name of the view we created in mysql.
