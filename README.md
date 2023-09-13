# fm_system
fm_system Django  project 폴더 
<br>
(2)> py -3.10 -m venv .venv10 <br>
(3)> .venv10\Scripts\activate <br>
(4)>(.venv) python -m pip install --upgrade pip <br>
(5)>(.venv) pip install django <br>
(6)>(.venv) pip install django-cors-headers <br>
(7)>(.venv) pip install djangorestframework <br>

----------------------------------------------
## 가상환경 세팅
pip install mysqlclient <br>
pip install plotly <br>
pip install dash==2.1.0 <br>
pip install dash_renderer <br>
python -m pip install django_plotly_dash <br>
pip install channels <br>
 <br>
pip install opencv-python <br>
pip install torch <br>
pip install torchvision <br>
pip install pandas <br>
pip install pyyaml <br>
pip install ultralytics <br>
pip install paddlepaddle <br>
pip install "paddleocr>=2.0.1" <br>
pip install django-apscheduler <br>

-----------------------------------------
python manage.py makemigrations <br>
python manage.py migrate <br>
pythoh manage.py runserver <br>
-----------------------------------------
pip install werkzeug==0.16.1 <br>
pip install Flask==2.1.3 <br>
pip install werkzeug==2.0.1 <br>

-----------------------------------------
###################################################################################
# 공용 nas DB 와 연결
###################################################################################

0. 설치하기 <br>
```
pip install mysqlclient
```
### 위에 것이 설치되어 있어야만 커넥션 객체가 생길 수 있음.

1. 주석 달기
- visualization/models.py 에서 view클래스들 주석
- visualization/views.py 에서 import MonthSafetyCntView, from .dash 주석
   model_view 주석
- visualization/urls.py path  주석
- templates/visualization/statistics.html 전체 주석
- visualization/dash.py 전체 주석


2. dbever에서 연결하기 
<main>
host: nas.parkingplace.co.kr
port: 23306
database: jjjdb
ID: jjjid
PW: jjjpw

<properties>
allowpublickey 머시기 를 true로 바꾸기


3. 프로젝트 파일 바깥에서
c드라이브/db_setting/jjjdb.py


4. config/setting.py 수정
```
import sys
sys.path.append(r'C:\db_setting')
import jjjdb
DATABASES = jjjdb.DATABASES
 ```


5. db 연결 확인 후 주석 해제
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
-------------------------------------------------
주석 <br>
python manage.py makemigrations <br>
python manage.py migrate <br>
pythoh manage.py runserver <br>
----------------------------------------
주석해제
python manage.py makemigrations
python manage.py migrate
pythoh manage.py runserver
-- new_month_safetycnt_view<br>
CREATE VIEW new_month_safetycnt_view AS SELECT NULL AS id, MONTH(aa.attend_time) as 'month', sc.sc_code as 'code', COUNT(*) as 'code_count', vc.content as 'content' FROM attend_safety_check sc INNER JOIN visualization_codes vc ON sc.sc_code = vc.code
INNER JOIN attend_attendance aa ON sc.att_id_id = aa.att_id GROUP BY month(aa.attend_time), sc.sc_code;
-- select * from new_month_safetycnt_view;

