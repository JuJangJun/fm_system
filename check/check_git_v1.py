import subprocess
import socket
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import os, sys
main_dir = os.path.dirname(os.path.realpath(__file__))
yolov5_dir = os.path.join(main_dir, 'yolov5')
sys.path.insert(0, yolov5_dir)
import detect_v4


# protoFile = "pose_deploy_linevec.prototxt" # test111.ipynb에서 test할때
# weightsFile = "pose_iter_160000.caffemodel" #
protoFile = "check\pose_deploy_linevec.prototxt" # 0.connect_model에서 runserver할때
weightsFile = "check\pose_iter_160000.caffemodel" #

load_openpose_start = time.time()
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile) # 0.5
load_openpose_end = time.time()


class Model():
    # self.check_openpose = check_openpose(image_route)
    # self.check_yolo = check_yolo(image_route)
########################################################################################
    def check_openpose(image):
        

        # protoFile = "pose_deploy_linevec.prototxt" # test111.ipynb에서 test할때
        # weightsFile = "pose_iter_160000.caffemodel" #
        # # protoFile = "check\pose_deploy_linevec.prototxt" # 0.connect_model에서 runserver할때
        # # weightsFile = "check\pose_iter_160000.caffemodel" #

        # load_openpose_start = time.time()
        # net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile) # 0.5
        # load_openpose_end = time.time()
        print(f"openpose model load time : {load_openpose_end-load_openpose_start}")

        # image = cv2.imread(image_route)


        # imageHeight, imageWidth, _ = image.shape
        imageWidth  = 368#이미지 사이즈를 줄이면 확실히 시간이 줄어들지만 정확도도 확연히 줄어든다.
        imageHeight = 368#정안될것같아서 많이 적확했던 640이 아닌 334로 타협을 했다. 

        inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False) #0.08

        net.setInput(inpBlob)


        #############################################
        test_start = time.time()
        output = net.forward() #여기가 18초가량 시간이 걸림->6초이내로 줄여짐
        test_end = time.time()
        print(f"time test : {test_end-test_start}")
        #############################################

        H = output.shape[2]
        W = output.shape[3]
        print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ", output.shape[3])


        points = []

        X=[]
        Y=[]

        for i in range(0, 15):
            

            probMap = output[0, i, :, :]


            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)


            x = (imageWidth * point[0]) / W
            y = (imageHeight * point[1]) / H
            if i==0:
                y-=10 #헬멧을 탐지 못할때 조금 더 패딩값을 준것이다 (머리윗부분한정으로)
            X.append(x)
            Y.append(y)

        return X,Y

    

########################################################################################
    # yolov5
    def check_yolo(image):

        result = []
        result = detect_v4.my_run(image)
        
        print("check_yolo result : ",result)

        return result



########################################################################################
    # main계산
    def calculate(image):
        warning_code = ""
        start = time.time()
        
        X,Y= Model.check_openpose(image)

        openpose = time.time()

        bboxes= Model.check_yolo(image)

        yolo = time.time()

        print("out_X : ", X)
        print("out_Y : ", Y)
        print("bboxes : ", bboxes)
        print("계산시작지점")


        #openpose로 만든 정답구역 #여기서 나중에 생각을 다시 해봐야될수도있다. min <=> max
        head = X[0], Y[0]
        neck = X[1], Y[1]
        Rhip = X[8], Y[8]
        Lhip = X[11], Y[11]
        Rshoulder = X[2], Y[2]

        a=(head[1]-neck[1])/2
        xmin = head[0]-a
        xmax = head[0]+a
        ymin = Y[1]
        ymax = Y[0]

        xmin2, xmax2, ymin2, ymax2 = Rhip[0], Lhip[0], Lhip[1], Rshoulder[1]

        c0, c1, c3 = 0,0,0 #탐지된 클래스의 수

        warning_code = "N : 모두다 착용함" #리턴할 최종 경고코드 디폴트는 다 있다로 해놓는다.
        #아래에서 없는경우의 수를 체크해서 warning_code값을 수정할것이다.

        cal = time.time()

        for i in range(len(bboxes[0])): #탐지된 박스 수만큼 돌아갈것이다.

            print(f"{i}번째 for문")
            box = bboxes[0][i][:4] #i번째의 박스 좌표
            xmean = np.mean([box[0], box[2]]) #박스 중앙 x,y값
            ymean = np.mean([box[0], box[2]])
            
            if bboxes[0][i][-1] == 0.0: #고글 (머리박스와 비교)
                print(bboxes[0][i][-1])
                if ((xmax<xmean<xmin)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("통과")
                else:
                    pass
                print("-----0고글탐지됨-----")
                c0 += 1


            elif bboxes[0][i][-1] == 3.0: #헬멧 (머리박스와 비교)
                print(bboxes[0][i][-1])
                if ((xmax<xmean<xmin)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("통과")

                else:
                    pass
                print("-----3헬멧탐지됨-----")
                c3 += 1


            elif bboxes[0][i][-1] == 1.0: #조끼 (몸통박스와 비교)
                print(bboxes[0][i][-1])
                if ((xmax2<xmean<xmin2)&(ymax2<ymean<ymin2)): #min max자리바꿈
                        print("통과")

                else:

                    pass
                print("-----1조끼탐지됨-----")
                c1 += 1


        if c0 == 0:
            warning_code = "G : 고글없음, 헬멧/조끼있음"
            if c1== 0:
                warning_code = "VG : 조끼/고글없음, 헬멧있음"
            elif c3 == 0:
                warning_code = "HG : 헬멧/고글없음, 조끼있음"

        elif c1 == 0:
            warning_code = "V : 조끼없음, 헬멧/고글있음"
            if c3 == 0:
                warning_code = "HV : 헬멧/조끼없음, 고글있음"

        elif c3 == 0:
            warning_code = "H : 헬멧없음, 고글/조끼있음"

        print("최종리턴값 : " ,warning_code)
        end = time.time()

        print(f"openpose까지의 시간 : {openpose-start}")
        print(f"yolo까지의 시간 : {yolo-openpose}")
        print(f"계산까지의 시간 : {end-yolo}")

        return warning_code



