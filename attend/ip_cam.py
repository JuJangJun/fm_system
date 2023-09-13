import urllib.request
import cv2
import re
import numpy as np
import time
from check import check_v4, check_v4_yolov8
from collections import Counter
# from modules import change_contrast


# ################### url 연결 ###################
# url='http://192.168.0.174:8080/shot.jpg'

class IpCam():

    def last_return(l):
        cnt = Counter(l)
        return cnt.most_common()[0][0]
    

    def cam_2(url):
        # ocr = PaddleOCR()
        cnt = 0
        warning_code =""
        wear = ""
        start = time.time()
        l =[]

        while cnt<3:
            while_start = time.time()
            imgResp = urllib.request.urlopen(url)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp,-1)  # 뭐여
            print("이미지 원본사이즈 : ",img.shape)
            
            # # 이미지 사이즈 줄이기
            img = cv2.resize(img, (640 , 640), interpolation=cv2.INTER_AREA)
            
            cnt+=1
            # image = cv2.imread(img)
            # result = check_v4.Model.calculate(img)
            result = check_v4_yolov8.Model.calculate(img)
            l.append(result)
            while_end = time.time()
            print(f"{cnt}번째 while문 소요시간",while_end-while_start)
            print("l : ", l)

        warning_code = IpCam.last_return(l)
        print("최종 warning_code : ", warning_code)
        if warning_code == "G":
            wear = "헬멧, 조끼"
        elif warning_code == "VG":
            wear = "헬멧"
        elif warning_code == "HVG":
            wear = "모두착용하지않음"
        elif warning_code == "HG":
            wear = "조끼"
        elif warning_code == "V":
            wear = "헬멧, 고글"
        elif warning_code == "HV":
            wear = "고글"
        elif warning_code == "H":
            wear = "고글, 조끼"
        elif warning_code == "N":
            wear = "모두착용했습니다."

        end = time.time()
        print(f"총소요시간 : ",end-start)
        
        
        return {"wc" : warning_code, "wr" : wear}
