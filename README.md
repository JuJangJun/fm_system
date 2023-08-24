# fm_system
fm_system Django  project 폴더

# pip install
pip install paddlepaddle <br>
pip install "paddleocr>=2.0.1" <br>
pip install mysqlclient <br>

### mySQL 기본 데이터 삽입 코드 ###
-- visualization_code 테이블에 코드 정보 추가
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

-- attend_workers 테이블에 코드 정보 추가
INSERT INTO attend_workers values (501, '나승주', 419, '010-6601-9990', '335045@naver.com'), 
  (419, '장수연', NULL, '010-1234-xxxx', NULL), (531, '민경준', 419, '010-xxxx-0123', NULL);

-- access_place 테이블에 구역 정보 추가 
INSERT INTO access_place values ('A1', '위험하지 않은 구역 어딘가', 1, 1), ('A100', '위험 구역 어딘가', 5, 3), ('A50', '보통~', 3, 2);

