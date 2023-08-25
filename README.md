# fm_system
fm_system Django  project 폴더

## pip install
pip install paddlepaddle <br>
pip install "paddleocr>=2.0.1" <br>
pip install mysqlclient <br>

### mySQL 기본 데이터 삽입 코드 ###
use jjjdb;

#################### 사전 데이터 입력 ###########################
-- visualization_code 테이블에 코드 정보 추가<br>
insert into visualization_codes (code, content)
values
	('H', '헬멧 미착용'),
	('v', '조끼 미착용'),
	('G', '고글 미착용'),
	('HV', '헬멧, 조끼 미착용'),
	('HG', '헬멧, 고글 미착용'),
	('VG', '조끼, 고글 미착용'),
	('HVG', '전부 미착용'),
	('N', '모두 착용');
	

-- attend_workers 테이블에 코드 정보 추가<br>
INSERT INTO attend_workers values (501, '나승주', 419, '010-6601-9990', '335045@naver.com'), 
								  (419, '장수연', NULL, '010-1234-xxxx', NULL), 
								  (531, '민경준', 419, '010-xxxx-0123', NULL);

								 
-- access_place 테이블에 구역 정보 추가 <br>
INSERT INTO access_place values ('A1', '위험 x 구역', 1, 1), ('A100', '위험 구역', 5, 3);



#################### 필요한 뷰 생성###########################
-- new_month_safetycnt_view<br>
CREATE VIEW new_month_safetycnt_view AS SELECT NULL AS id, MONTH(aa.attend_time) as 'month', sc.sc_code as 'code', COUNT(*) as 'code_count', vc.content as 'content' FROM attend_safety_check sc INNER JOIN visualization_codes vc ON sc.sc_code = vc.code
INNER JOIN attend_attendance aa ON sc.att_id_id = aa.att_id GROUP BY month(aa.attend_time), sc.sc_code;
-- select * from new_month_safetycnt_view;

