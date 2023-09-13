# import subprocess
# import socket
# import pandas as pd
import cv2
# from matplotlib import pyplot as plt
import numpy as np
import time
import os, sys
main_dir = os.path.dirname(os.path.realpath(__file__))

from . import detect_yolov8

import cv2
import mediapipe as mp
import numpy as np



class Model():
    # self.check_openpose = check_openpose(image_route)
    # self.check_yolo = check_yolo(image_route)
########################################################################################
    def media_pipe(image):

        # mp.solutions : MediaPipe 라이브러리의 고수준 api 제공 모듈
        mp_drawing = mp.solutions.drawing_utils  # drawing_urils 모듈 mp_drawing 변수에 할당
        mp_drawing_styles = mp.solutions.drawing_styles  # drawing_styles 모듈은 랜드마크와 연결선들을 그릴 때 사용되는 스타일(색상, 선 굵기 등)을 정의하는 도구를 제공
        mp_pose = mp.solutions.pose  # pose 모듈을 mp_pose 변수에 할당,  pose 솔루션은 이미지나 비디오에서 사람 몸의 포즈(pose)를 추정하기 위해 사용
        ### mp_pose만 설정하면 될듯 !! 우리는 그림은 안그릴 것이기 때문


        BG_COLOR = (192, 192, 192)  # 회색
        # image = r"C:\div\Django_tutorial\0.connect_model\check\yolov5\1.jpg"  # 이미지 경로

        ## mp_pose.Pose 객체 생성, 초기화
        with mp_pose.Pose(
                static_image_mode=True,    # 사진일 때 이 설정
                model_complexity=2,        # model_complexity=2: 모델 복잡도
                enable_segmentation=True,  # 분할 마스크(segmentation mask) 활성화 여부
                min_detection_confidence=0.5) as pose:  # 포즈 감지에 대한 최소 신뢰도 임계값

            # image = cv2.imread(image)
            # image_height, image_width, _ = image.shape
            image_height, image_width = 640, 640

            print(image_height, image_width)
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            print("results : ", results)
            print("resultstype",type(results))
            
            try: 
                Rhip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height
                Rshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height
                Lshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
                print("Rhip", Rhip)
                print("Rshoulder", Rshoulder)
                print("Lshoulder", Lshoulder)

                xmin = Rshoulder[0]
                xmax = Lshoulder[0]
                ymin = Rshoulder[1]
                ymax = Rshoulder[1] - (Lshoulder[0]-Rshoulder[0]) -120

                xmin2 = Rhip[0]
                xmax2 = Lshoulder[0]
                ymin2 = Rhip[1]
                ymax2 = Lshoulder[1]

                return xmin, xmax, ymin, ymax, xmin2, xmax2, ymin2, ymax2
            except:
                xmin, xmax, ymin, ymax, xmin2, xmax2, ymin2, ymax2 = None, None, None, None, None, None, None, None
                return xmin, xmax, ymin, ymax, xmin2, xmax2, ymin2, ymax2
    
            # return Rhip, Rshoulder,Lshoulder

########################################################################################
    # yolov5
    def check_yolo(image):

        result = []
        result = detect_yolov8.Model(image)
        
        print("check_yolo result : ",result)

        return result


########################################################################################
    # main계산
    def calculate(image):
        warning_code = ""
        wear = ""
        start = time.time()
        
        X,Y = [], []
        # X1,Y1= Model.check_openpose(image)
        # X,Y= Model.check_openpose(image)
        xmin, xmax, ymin, ymax, xmin2, xmax2, ymin2, ymax2 = Model.media_pipe(image)


        media_pipe = time.time()
        
        bboxes= Model.check_yolo(image)
        if bboxes == []:
            warning_code = "HVG"
            return warning_code

        yolo = time.time()
        print("bboxes : ", bboxes)
        print("계산시작지점")


        if xmin == None:
            print("xmin 못찾음")
            warning_code = "HVG"
            return warning_code
        if xmax == None:
            print("xmax 못찾음")
            warning_code = "HVG"
            return warning_code
        if ymin == None:
            print("ymin 못찾음")
            warning_code = "HVG"
            return warning_code
        if ymax == None:
            print("ymax 못찾음")
            warning_code = "HVG"
            return warning_code
        
        if xmin2 == None:
            print("xmin2 못찾음")
            warning_code = "HVG"
            return warning_code
        if xmax2 == None:
            print("xmax2 못찾음")
            warning_code = "HVG"
            return warning_code
        if ymin2 == None:
            print("ymin2 못찾음")
            warning_code = "HVG"
            return warning_code
        if ymax2 == None:
            print("ymax2 못찾음")
            warning_code = "HVG"
            return warning_code






        c0, c1, c2 = 0,0,0 #탐지된 클래스의 수

        warning_code = "N" #리턴할 최종 경고코드 디폴트는 다 있다로 해놓는다.
        wear = "헬멧, 고글, 조끼"
        #아래에서 없는경우의 수를 체크해서 warning_code값을 수정할것이다.


        print("xmin : ", xmin, "/ xmax : ", xmax, "/ ymin : ", ymin, "/ ymax : ", ymax)
        print("xmin2 : ", xmin2, "/ xmax2 : ", xmax2, "/ ymin2 : ", ymin2, "/ ymax2 : ", ymax2)
        print("탐지된 박스의 개수 :",len(bboxes))
        print("bboxes : ", bboxes)
        print("탐지된 박스의 개수 :",len(bboxes))

        cal = time.time()

        for i in range(len(bboxes)): #탐지된 박스 수만큼 돌아갈것이다.

            print(f"{i}번째 for문")
            xmean = bboxes[i][0][0]
            ymean = bboxes[i][0][1]
            objects = bboxes[i][1]
            print(f"{i}번째 박스",xmean, ymean, objects)
            
            if objects == 1.0: #고글 (머리박스와 비교)
                print("여기는 고글(0) : ",objects)
                if ((xmin<xmean<xmax)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("고글통과")
                        c0 += 1
                else:
                    print("다시 착용 요망")
                


            elif objects == 3.0: #헬멧 (머리박스와 비교)
                print("여기는 헬멧(2) : ",objects)
                if ((xmin<xmean<xmax)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("헬멧통과")
                        c2 += 1
                else:
                    print("다시 착용 요망")
                


            elif objects == 4.0: #조끼 (몸통박스와 비교)
                print("여기는 조끼(3) : ",objects)
                if ((xmin2<xmean<xmax2)&(ymax2<ymean<ymin2)): #min max자리바꿈
                        print("조끼통과")
                        c1 += 1
                else:
                    print("다시 착용 요망")
                
                
            print("c0 : ",c0)
            print("c1 : ",c1)
            print("c2 : ",c2)

        if c0 == 0:
            warning_code = "G"
            wear = "헬멧, 조끼"
            if c1 == 0:
                warning_code = "VG"
                wear = "헬멧"
                if c2 == 0:
                    warning_code = "HVG"
                    wear = "모두착용하지않음"
            elif c2 == 0:
                warning_code = "HG"
                wear = "조끼"
                if c1 == 0:
                    warning_code = "HVG"
                    wear = "모두착용하지않음"

        elif c1 == 0:
            warning_code = "V"
            wear = "헬멧, 고글"
            if c2 == 0:
                warning_code = "HV"
                wear = "고글"

        elif c2 == 0:
            warning_code = "H"
            wear = "고글, 조끼"

        print("최종리턴값 : " ,warning_code)
        end = time.time()

        print(f"mediapipe까지의 시간 : {media_pipe-start}")
        print(f"yolov8까지의 시간 : {yolo-media_pipe}")
        print(f"계산까지의 시간 : {end-yolo}")
        print(f"모델 총 시간 : , {end-start}")

        return warning_code

