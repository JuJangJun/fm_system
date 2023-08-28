# import subprocess
# import socket
# import pandas as pd
import cv2
# from matplotlib import pyplot as plt
import numpy as np
import time
import os, sys
main_dir = os.path.dirname(os.path.realpath(__file__))
yolov5_dir = os.path.join(main_dir, 'yolov5')
sys.path.insert(0, yolov5_dir)
# from yolov5 import detect_v4
import detect_v4

# BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
#                     "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
#                     "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
#                     "Background": 15}

# POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
#             ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
#             ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
#             ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]

# protoFile = "pose_deploy_linevec.prototxt" # test111.ipynb에서 test할때
# weightsFile = "pose_iter_160000.caffemodel" #
# protoFile = "check\pose_deploy_linevec.prototxt" # 0.connect_model에서 runserver할때
# weightsFile = "check\pose_iter_160000.caffemodel" #

# load_openpose_start = time.time()
# net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile) # 0.5
# load_openpose_end = time.time()


class Model():
    # self.check_openpose = check_openpose(image_route)
    # self.check_yolo = check_yolo(image_route)
########################################################################################
    def check_openpose(image):
        

        # protoFile = "pose_deploy_linevec.prototxt" # test111.ipynb에서 test할때
        # weightsFile = "pose_iter_160000.caffemodel" #
        protoFile = "check\pose_deploy_linevec.prototxt" # 0.connect_model에서 runserver할때
        weightsFile = "check\pose_iter_160000.caffemodel" #

        # load_openpose_start = time.time()
        # net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile) # 0.5
        # load_openpose_end = time.time()

        ################################################################################################################################################
        # print(f"openpose model load time : {load_openpose_end-load_openpose_start}")

        # # image = cv2.imread(image_route)


        # # imageHeight, imageWidth, _ = image.shape
        # imageWidth  = 368#이미지 사이즈를 줄이면 확실히 시간이 줄어들지만 정확도도 확연히 줄어든다.
        # imageHeight = 368#정안될것같아서 많이 적확했던 640이 아닌 334로 타협을 했다. 
        # # 352, 416,             480, 512, 544, 576,       608,       640
        # inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False) #0.08

        # net.setInput(inpBlob)


        # #############################################
        # test_start = time.time()
        # output = net.forward() #여기가 18초가량 시간이 걸림->6초이내로 줄여짐
        # test_end = time.time()
        # print(f"time test : {test_end-test_start}")
        # #############################################

        # H = output.shape[2]
        # W = output.shape[3]
        # print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ", output.shape[3])


        # points = []

        # X=[]
        # Y=[]

        # for i in range(0, 15):
            

        #     probMap = output[0, i, :, :]


        #     minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)


        #     x = (imageWidth * point[0]) / W
        #     y = (imageHeight * point[1]) / H
        #     if i==0:
        #         y-=10 #헬멧을 탐지 못할때 조금 더 패딩값을 준것이다 (머리윗부분한정으로)
        #     X.append(x)
        #     Y.append(y)

            ##########################################################################################################################################
        # X = [240.0, 240.0, 208.0, 160.0, 176.0, 280.0, 328.0, 312.0, 232.0, 240.0, 240.0, 272.0, 280.0, 288.0, 248.0]
        # Y = [134.0, 184.0, 208.0, 232.0, 184.0, 200.0, 232.0, 184.0, 344.0, 448.0, 528.0, 344.0, 440.0, 528.0, 272.0]
            ##########################################################################################################################################
        # protoFile = "pose_deploy_linevec.prototxt" # test111.ipynb에서 test할때
        # weightsFile = "pose_iter_160000.caffemodel" #
        # protoFile = "check\pose_deploy_linevec.prototxt" # 0.connect_model에서 runserver할때
        # weightsFile = "check\pose_iter_160000.caffemodel" #

        # model = "pose_iter_160000.caffemodel"# test111.ipynb에서 test할때
        # config = "pose_deploy_linevec.prototxt"
        # config = "pose_deploy_linevec_faster_4_stages.prototxt"
        
        model = "check\pose_iter_160000.caffemodel"# 0.connect_model에서 runserver할때
        # # config = "check\pose_deploy_linevec.prototxt"
        config = "check\pose_deploy_linevec_faster_4_stages.prototxt"

        # 포즈 점 개수, 점 연결 개수, 연결 점 번호 쌍
        nparts = 18
        # npairs = 17
        net = cv2.dnn.readNet(model, config)
        
        blob = cv2.dnn.blobFromImage(image, 1 / 255., (368, 368))
        net.setInput(blob)

        start = time.time()
        out = net.forward()  # out.shape=(1, 57, 46, 46)
        end = time.time()
        print("foward시간 : ",end-start)

        # h, w = image.shape[:2]
        h, w = 368,368

        # 검출된 점 추출
        points = []
        for i in range(nparts):
            heatMap = out[0, i, :, :]
            # 최댓값을 conf에 넣어준다.
            _, conf, _, point = cv2.minMaxLoc(heatMap)
            x = int(w * point[0] / out.shape[3])
            y = int(h * point[1] / out.shape[2])

            points.append((x, y) if conf > 0.1 else None) 













            # print(f"{i}번째점 = x:{x},   y:{y},    334-y :{334-y}")
            # print(f"point : {point}")
            # print("--------------------------")



            # if prob > 0.1:
            #     cv2.circle(image, (int(x), int(y)), 3, (0, 255, 255), thickness=-1,
            #             lineType=cv2.FILLED)
            #     cv2.putText(image, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
            #                 lineType=cv2.LINE_AA)
            #     points.append((int(x), int(y)))
            # else:
            #     points.append(None)

        # cv2.imshow("Output-Keypoints", image) # cv2.imshow() 대신 cv2_imshow()을 사용합니다.
        # cv2_imshow(image)
        # cv2.imshow(" ",image)


        # imageCopy = image


        # for pair in POSE_PAIRS:
        #     partA = pair[0]
        #     partA = BODY_PARTS[partA]
        #     partB = pair[1]
        #     partB = BODY_PARTS[partB]
        #     if points[partA] and points[partB]:
        #         cv2.line(imageCopy, points[partA], points[partB], (0, 255, 0), 2)

        
        # cv2.imshow("Output-Keypoints", imageCopy) # cv2.imshow() 대신 cv2_imshow()을 사용합니다.
        
        # cv2_imshow(imageCopy)
        # cv2.imshow(imageCopy)
        # cv2.destroyAllWindows()
        # print(x,y)

        # print("in_X : ", X)
        # print("in_Y : ", Y)
        return points
        return X,Y
    # # openpose
    # def check_openpose(self.image):
    #     # from google.colab.patches import cv2_imshow
        
    #     X,Y= self.print_hi(self.image)
        
    #     return X,Y

    # print(check_openpose(image_route)) #해당이미지를 잘 확인하는지 볼 수 있다.

    # X,Y = check_openpose(image_route)
    # print("out_X : ", X)
    # print("out_Y : ", Y)
    # 위의 세 코드를 통해서 함수 밖으로 X,Y좌표들을 뽑아낼 수 있다는걸 확인 할 수 있다.

    #check_openpose는 잘 굴러가는걸 확인이 된다. => 결과값 X , Y

    

########################################################################################
    # yolov5
    def check_yolo(image):
        # print("이미지경로 : ", image_route)
        # 이미지경로를 변수로 사용하려면 {}를 사용하면 된다.
        # p = !python C:\Users\Playdata\Desktop\vscod\detect_v3.py  --weights C:\Users\Playdata\Desktop\vscod\best1.pt --img 334 --conf 0.4 --source {image_route}
        # p = my_run(image_route)

        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_socket.bind(('127.0.0.1', 12345))

        # server_socket.listen(1)

        # p = detect_v4.main()
        result = []
        result = detect_v4.my_run(image)
        
        print("check_yolo result : ",result)
        # np.array(result[0][:4]).astype(int) #얘는 박스 좌표만 뽑고 싶은거야 클래스 뽑으려면 아마[5]일것이다.
        # list(map(int, result[0][:4]))#리스트로 변경
        # print("변경후 result : ",result)
    
        # print(p)
        # subprocess.check_output(r"python C:\Users\Playdata\Desktop\vscod\check\yolov5\detect_v4.py --weights C:\Users\Playdata\Desktop\vscod\best1.pt --img 334 --conf 0.4 --source {image_route}".format(image_route=image_route),
        #     ['python' ,r'C:\Users\Playdata\Desktop\vscod\check\detect_v4.py', r'--weights C:\Users\Playdata\Desktop\vscod\best1.pt --img 334 --conf 0.4 --source {image_route}'.format(image_route=image_route)],
        #     shell=False)

        # connetion_sock, addr = server_socket.accept()

        # data = connetion_sock.recv(1024)

        # connetion_sock.close()
        # server_socket.close()

        # df = pd.read_json(data.decode('utf-8'))
        # p = df['data'][0]

        # return p
        # if len(result)==0: #만약 아무것도 탐지되지 않았으면
        #     print("다시 장비를 착용해주십시오")
        #     answer ="다시 장비를 착용해주십시오"
        #     return answer
        
        # print("len",len(result[0]))
        # bboxes = []
        # box_class = []
        # for i in range(len(result[0])):
        #     bboxes.append(result[0][i][:4])
        #     box_class.append(result[0][i][-1])
        # print("bboxes : ",bboxes)
        # print("box_class : ", box_class)

        # for i in range(len(eval(p[-1])[0])):
        #     bboxes.append(eval(p[-1])[0][i][:4])

        # xmean = np.mean(bboxes[0][0],bboxes[0][2])
        # ymean = np.mean(bboxes[0][1],bboxes[0][3])
        # print(bboxes)

        # return bboxes
        # return bboxes, box_class
        return result

    # print(check_yolo(image_route))
    # bboxes = check_yolo(image_route)
    # print(bboxes)

    #check_yolo도 잘 굴러간다.  => 결과값 : bboxes = [ [박스좌표1], [박스좌표2], [박스좌표2]..... ]


########################################################################################
    # main계산
    def calculate(image):
        warning_code = ""
        wear = ""
        start = time.time()
        
        X,Y = [], []
        # X1,Y1= Model.check_openpose(image)
        # X,Y= Model.check_openpose(image)
        points = Model.check_openpose(image)


        #368이미지를 openpose로 측정한 좌표를 640이미지에 적용한다.
        # for i in X1:
        #     X.append(round(i/368*640, 0))
        # for j in Y1:
        #     Y.append(round(j/368*640, 0))
        # print("XX : ",X)
        # print("YY : ",Y)

        openpose = time.time()

        bboxes= Model.check_yolo(image)
        if bboxes == []:
            # return "아무것도 탐지되지 않았습니다."
            warning_code = "HVG"
            return warning_code
        
        # if bboxes =="다시 장비를 착용해주십시오":
        #     answer ="다시 장비를 착용해주십시오"
        #     warning_code = "HVG"
        #     return answer, warning_code

        yolo = time.time()

        # print("out_X : ", X)
        # print("out_Y : ", Y)
        print("points : ", points)
        print("bboxes : ", bboxes)
        print("계산시작지점")


        #openpose로 만든 정답구역 #여기서 나중에 생각을 다시 해봐야될수도있다. min <=> max
        # head = X[0], Y[0]-50
        # neck = X[1], Y[1]
        # print("head : ", head)
        # print("neck : ", neck)
        # Rhip = X[8], Y[8]
        # Lhip = X[11], Y[11]
        # Rshoulder = X[2], Y[2]
        # Lshoulder = X[5], Y[5]
        head = points[0][0],points[0][1]-50
        neck = points[1]
        Rhip = points[8]
        Lshoulder = points[5]
        if head == []:
            warning_code = "HVG"
            return warning_code
        if neck == []:
            warning_code = "HVG"
            return warning_code
        if Rhip == []:
            warning_code = "HVG"
            return warning_code
        if Lshoulder == []:
            warning_code = "HVG"
            return warning_code
        # head, neck, Rhip, Lshoulder




        a=(neck[1]-head[1])/2
        print("a : ", a)
        xmin = head[0]-a
        xmax = head[0]+a
        ymin = neck[1]
        ymax = head[1]

        xmin2 = Rhip[0]
        xmax2 = Lshoulder[0]
        ymin2 = Rhip[1]
        ymax2 = Lshoulder[1]

        c0, c1, c3 = 0,0,0 #탐지된 클래스의 수

        warning_code = "N" #리턴할 최종 경고코드 디폴트는 다 있다로 해놓는다.
        wear = "헬멧, 고글, 조끼"
        #아래에서 없는경우의 수를 체크해서 warning_code값을 수정할것이다.

        # #변수체크
        # print("xmin : ", xmin, "xmax : ", xmax, "ymin : ", ymin, "ymax : ", ymax)
        # print("탐지된 박스의 개수 : ", len(bboxes))
        print("xmin : ", xmin, "/ xmax : ", xmax, "/ ymin : ", ymin, "/ ymax : ", ymax)
        print("xmin2 : ", xmin2, "/ xmax2 : ", xmax2, "/ ymin2 : ", ymin2, "/ ymax2 : ", ymax2)
        print("탐지된 박스의 개수 :",len(bboxes))
        print("bboxes : ", bboxes)
        # print("bboxes[0] : ", bboxes[0])
        print("탐지된 박스의 개수 :",len(bboxes))

        cal = time.time()

        for i in range(len(bboxes)): #탐지된 박스 수만큼 돌아갈것이다.

            print(f"{i}번째 for문")
            xmean = np.mean([bboxes[i][0], bboxes[i][2]])/640*368
            ymean = np.mean([bboxes[i][1], bboxes[i][3]])/640*368
            print("xmean : ", xmean, "ymean :", ymean)
            
            if bboxes[i][-1] == 0.0: #고글 (머리박스와 비교)
                print("여기는 고글(0) : ",bboxes[i][-1])
                if ((xmin<xmean<xmax)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("고글통과")
                        c0 += 1
                else:
                    print("다시 착용 요망")
                


            elif bboxes[i][-1] == 3.0: #헬멧 (머리박스와 비교)
                print("여기는 헬멧(3) : ",bboxes[i][-1])
                if ((xmin<xmean<xmax)&(ymax<ymean<ymin)): #min max자리바꿈
                        print("헬멧통과")
                        c3 += 1
                else:
                    print("다시 착용 요망")
                


            elif bboxes[i][-1] == 1.0: #조끼 (몸통박스와 비교)
                print("여기는 조끼(1) : ",bboxes[i][-1])
                if ((xmin2<xmean<xmax2)&(ymax2<ymean<ymin2)): #min max자리바꿈
                        print("조끼통과")
                        c1 += 1
                else:
                    print("다시 착용 요망")
                
                
            print("c0 : ",c0)
            print("c1 : ",c1)
            print("c3 : ",c3)

        # if c0 == 0:
        #     warning_code = "G : 고글없음, 헬멧/조끼있음"
        #     if c1== 0:
        #         warning_code = "VG : 조끼/고글없음, 헬멧있음"
        #     elif c3 == 0:
        #         warning_code = "HG : 헬멧/고글없음, 조끼있음"

        # elif c1 == 0:
        #     warning_code = "V : 조끼없음, 헬멧/고글있음"
        #     if c3 == 0:
        #         warning_code = "HV : 헬멧/조끼없음, 고글있음"

        # elif c3 == 0:
        #     warning_code = "H : 헬멧없음, 고글/조끼있음"

        if c0 == 0:
            warning_code = "G"
            wear = "헬멧, 조끼"
            if c1 == 0:
                warning_code = "VG"
                wear = "헬멧"
                if c3 == 0:
                    warning_code = "HVG"
                    wear = "모두착용하지않음"
            elif c3 == 0:
                warning_code = "HG"
                wear = "조끼"
                if c1 == 0:
                    warning_code = "HVG"
                    wear = "모두착용하지않음"

        elif c1 == 0:
            warning_code = "V"
            wear = "헬멧, 고글"
            if c3 == 0:
                warning_code = "HV"
                wear = "고글"

        elif c3 == 0:
            warning_code = "H"
            wear = "고글, 조끼"

        print("최종리턴값 : " ,warning_code)
        end = time.time()

        print(f"openpose까지의 시간 : {openpose-start}")
        print(f"yolo까지의 시간 : {yolo-openpose}")
        print(f"계산까지의 시간 : {end-yolo}")
        print(f"모델 총 시간 : , {end-start}")
        # p  = {"wc" : warning_code, "wr":wear}

        return warning_code
        # return warning_code, wear
        # return p
    
        # #최종비교
        # count = 0
        
        # print("cal bboxes : ",(len(bboxes[0])))
        # print("bboxes : ", bboxes)
        # print("bboxes[0] : ", bboxes[0])
        # for i in range(len(bboxes)):
        #     xmean = np.mean([bboxes[i][0], bboxes[i][2]])
        #     ymean = np.mean([bboxes[i][1], bboxes[i][3]])

        #     print("xmean : ", xmean)
        #     print("ymean : ", ymean)

        #     if ((xmax<xmean<xmin)&(ymax<ymean<ymin)): #min max자리바꿈
        #         print("통과")
        #         count+=1
        #         # if ((xmin<xmean<xmax)&(ymin<ymean<ymax)):
        #     else:
        #         # print("다시 착용 요망")
        #         pass

        # if count>0:
        #     print("최종통과되셨습니다.")
        #     answer="최종통과되셨습니다."

        #     for a in box_class:
        #         c0 = 0
        #         c1 = 0
        #         c3 = 0
        #         for a in box_class:
        #             if a== 0.0:
        #                 c0 +=1
        #             if a== 1.0:
        #                 c1 +=1
        #             if a== 3.0:
        #                 c3 +=1
        #         print(c0, c1, c3)

        #         worning_code = "N"

        #         if c0 == 0:
        #             worning_code = "G"
        #             if c1== 0:
        #                 worning_code = "VG"
        #             elif c3 == 0:
        #                 worning_code = "HG"

        #         elif c1 == 0:
        #             worning_code = "V"
        #             if c3 == 0:
        #                 worning_code = "HV"

        #         elif c3 == 0:
        #             worning_code = "H"

        #         print(worning_code)


        
        if count==0:
            print("다시 장비를 착용해주십시오")
            answer ="다시 장비를 착용해주십시오"
            warning_code = "HVG"
            return answer,warning_code

        end = time.time()

        print(f"openpose까지의 시간 : {openpose-start}")
        print(f"yolo까지의 시간 : {yolo-openpose}")
        print(f"계산까지의 시간 : {end-yolo}")



