from ultralytics import YOLO
import time
# model = YOLO("../yolov8_test/yolov8s_loadaws_add_680data_customdata_86epoc.pt")
model = YOLO(r"C:\Users\Playdata\Desktop\fm_system\check\loadaws_add_680data_custom106_hat117_glasses100_custom66_aug_7737_editclass_yolov8n_155epoc.pt")
# model = YOLO(r"C:\Users\Playdata\Desktop\fm_system\check\loadaws_add_680data_custom106_hat117_glasses100_custom66_aug_7737_editclass_yolov8_earlystop116.pt")

def Model(image):
    
    
    # print(type(model.names), len(model.names))
    print("yolov8 모델클래스 : ",model.names)

    start = time.time()
    results = model.predict(image)
    end = time.time()
    print("모델 탐지 시간 :",end-start)


    result = results[0]
    boxes = result.boxes.numpy()

    print("탐지된 박스의 개수",len(boxes))

    result = []
    for i in range(len(boxes)):
        box = []
        print(f"{i+1}번째박스")

        box.append(boxes.xywh[i][:2])
        box.append(boxes.cls[i])
        # print(box)
        
        result.append(box)
        print("yolov8내부 박스 result : ",result)

        print("-----------")
    return result
    # return boxes