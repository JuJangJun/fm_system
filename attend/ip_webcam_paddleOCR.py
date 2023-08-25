import urllib.request
import cv2
import numpy as np
import time
from pOCR import OCRmodel
# from modules import change_contrast


url='http://192.168.0.174:8080/shot.jpg'
# ocr = OCRmodel()

def Webcam():
    while True:
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp,-1)  # 뭐여
        
        # 이미지 사이즈 줄이기
        img = cv2.resize(img, (720, 486), interpolation=cv2.INTER_AREA)

        ######################################
        # OCR 실행
        # text, confidence = ocr.recognize(img)
        # print(text, confidence)
        
        time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    # return text, confidence
