class Check():
    # self.check_openpose = check_openpose(image_route)
    # self.check_yolo = check_yolo(image_route)
########################################################################################
    # openpose
    def check_openpose(self, image_route):
        # from google.colab.patches import cv2_imshow
        import cv2
        from matplotlib import pyplot as plt

        def print_hi(name):
            BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                        "Background": 15}

            POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                        ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                        ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]


            protoFile = "/content/drive/MyDrive/openpose/models/pose/mpi/pose_deploy_linevec.prototxt"
            weightsFile = "/content/drive/MyDrive/openpose/models/pose/mpi/pose_iter_160000.caffemodel"


            net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)


            image = cv2.imread(image_route)


            imageHeight, imageWidth, _ = image.shape


            inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False)


            net.setInput(inpBlob)


            output = net.forward()


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
                X.append(x)
                Y.append(y)
                # print(f"{i}번째점 = x:{x},   y:{y},    334-y :{334-y}")
                # print(f"point : {point}")
                # print("--------------------------")



                if prob > 0.1:
                    cv2.circle(image, (int(x), int(y)), 3, (0, 255, 255), thickness=-1,
                            lineType=cv2.FILLED)
                    cv2.putText(image, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                                lineType=cv2.LINE_AA)
                    points.append((int(x), int(y)))
                else:
                    points.append(None)

            # cv2.imshow("Output-Keypoints", image) # cv2.imshow() 대신 cv2_imshow()을 사용합니다.
            # cv2_imshow(image)
            cv2.imshow(image)


            imageCopy = image


            for pair in POSE_PAIRS:
                partA = pair[0]
                partA = BODY_PARTS[partA]
                partB = pair[1]
                partB = BODY_PARTS[partB]
                if points[partA] and points[partB]:
                    cv2.line(imageCopy, points[partA], points[partB], (0, 255, 0), 2)

            
            # cv2.imshow("Output-Keypoints", imageCopy) # cv2.imshow() 대신 cv2_imshow()을 사용합니다.
            
            # cv2_imshow(imageCopy)
            cv2.imshow(imageCopy)
            cv2.destroyAllWindows()
            # print(x,y)

            # print("in_X : ", X)
            # print("in_Y : ", Y)
            return X,Y


        if __name__ == '__main__':



            X,Y=print_hi('PyCharm')
            return X,Y
    # print(check_openpose(image_route)) #해당이미지를 잘 확인하는지 볼 수 있다.

    # X,Y = check_openpose(image_route)
    # print("out_X : ", X)
    # print("out_Y : ", Y)
    # 위의 세 코드를 통해서 함수 밖으로 X,Y좌표들을 뽑아낼 수 있다는걸 확인 할 수 있다.

    #check_openpose는 잘 굴러가는걸 확인이 된다. => 결과값 X , Y

    

########################################################################################
    # yolov5
    def check_yolo(self,image_route):
        # print("이미지경로 : ", image_route)
        # 이미지경로를 변수로 사용하려면 {}를 사용하면 된다.
        p = !python C:\Users\Playdata\Desktop\vscod\detect_v3.py  --weights C:\Users\Playdata\Desktop\vscod\best1.pt --img 334 --conf 0.4 --source {image_route}
        print(p[-2])

        bboxes = []
        for i in range(len(eval(p[-1])[0])):
            bboxes.append(eval(p[-1])[0][i][:4])

        # xmean = np.mean(bboxes[0][0],bboxes[0][2])
        # ymean = np.mean(bboxes[0][1],bboxes[0][3])
        # print(bboxes)

        return bboxes

    # print(check_yolo(image_route))
    # bboxes = check_yolo(image_route)
    # print(bboxes)

    #check_yolo도 잘 굴러간다.  => 결과값 : bboxes = [ [박스좌표1], [박스좌표2], [박스좌표2]..... ]


########################################################################################
    # main계산
    def calculate(self,image_route):
        import numpy as np
        X,Y = self.check_openpose(image_route)
        bboxes = self.check_yolo(image_route)
        print("out_X : ", X)
        print("out_Y : ", Y)
        print("bboxes : ", bboxes)
        print("계산시작지점")


        #openpose로 만든 정답구역 #여기서 나중에 생각을 다시 해봐야될수도있다. min <=> max
        head = X[0], Y[0]
        neck = X[1], Y[1]
        a=(head[1]-neck[1])/2
        xmin = head[0]-a
        xmax = head[0]+a
        ymin = Y[1]
        ymax = Y[0]

        #변수체크
        print("xmin : ", xmin, "xmax : ", xmax, "ymin : ", ymin, "ymax : ", ymax)
        print("탐지된 박스의 개수 : ", len(bboxes))


        #최종비교
        count = 0
        for i in range(len(bboxes)):
            xmean = np.mean([bboxes[i][0], bboxes[i][2]])
            ymean = np.mean([bboxes[i][1], bboxes[i][3]])

            print("xmean : ", xmean)
            print("ymean : ", ymean)

            if ((xmax<xmean<xmin)&(ymax<ymean<ymin)): #min max자리바꿈
            # if ((xmin<xmean<xmax)&(ymin<ymean<ymax)):
                # print("통과")
                count+=1
            else:
                # print("다시 착용 요망")
                pass

        if count>0:
            print("최종통과되셨습니다.")
        if count==0:
            print("다시 장비를 착용해주십시오")



